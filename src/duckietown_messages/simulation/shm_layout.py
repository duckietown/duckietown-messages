"""Shared-memory layout helpers for gym world transport."""

from __future__ import annotations

import struct
from dataclasses import dataclass

__all__ = [
    "DEFAULT_WORLD_INPUT_MAX_BYTES",
    "DEFAULT_WORLD_OUTPUT_MAX_BYTES",
    "SHM_HEADER_FMT",
    "SHM_HEADER_SIZE",
    "SHM_MAGIC",
    "SHM_VERSION",
    "ShmLayout",
    "default_shm_layout",
    "pack_shm_header",
    "resize_shm_layout",
    "unpack_shm_header",
]

SHM_MAGIC = b"DMIO"
SHM_VERSION = 1
SHM_HEADER_FMT = "<4sIIIII"
SHM_HEADER_SIZE = struct.calcsize(SHM_HEADER_FMT)

# Keep the default slot modest and grow from runtime payload sizes.
DEFAULT_WORLD_INPUT_MAX_BYTES = 64 * 1024
DEFAULT_WORLD_OUTPUT_MAX_BYTES = 16 * 1024


@dataclass(frozen=True, slots=True)
class ShmLayout:
    """Layout of the SHM world I/O file."""

    world_input_capacity: int = DEFAULT_WORLD_INPUT_MAX_BYTES
    world_output_capacity: int = DEFAULT_WORLD_OUTPUT_MAX_BYTES

    def __post_init__(self) -> None:
        if self.world_input_capacity <= 0:
            message = "world_input_capacity must be positive."
            raise ValueError(message)
        if self.world_output_capacity <= 0:
            message = "world_output_capacity must be positive."
            raise ValueError(message)

    @property
    def total_size(self) -> int:
        return SHM_HEADER_SIZE + self.world_input_capacity + self.world_output_capacity

    @property
    def world_input_offset(self) -> int:
        return SHM_HEADER_SIZE

    @property
    def world_output_offset(self) -> int:
        return SHM_HEADER_SIZE + self.world_input_capacity


def default_shm_layout() -> ShmLayout:
    """Return the default SHM layout."""

    return ShmLayout()


def _grow_capacity(
    current_capacity: int,
    required_capacity: int,
    *,
    minimum_capacity: int,
) -> int:
    capacity = max(current_capacity, minimum_capacity, 1)
    while capacity < required_capacity:
        capacity *= 2
    return capacity


def resize_shm_layout(
    layout: ShmLayout,
    *,
    min_world_input_capacity: int | None = None,
    min_world_output_capacity: int | None = None,
) -> ShmLayout:
    """Grow the layout to fit the requested minimum capacities."""

    world_input_capacity = _grow_capacity(
        layout.world_input_capacity,
        min_world_input_capacity or 0,
        minimum_capacity=DEFAULT_WORLD_INPUT_MAX_BYTES,
    )
    world_output_capacity = _grow_capacity(
        layout.world_output_capacity,
        min_world_output_capacity or 0,
        minimum_capacity=DEFAULT_WORLD_OUTPUT_MAX_BYTES,
    )
    return ShmLayout(
        world_input_capacity=world_input_capacity,
        world_output_capacity=world_output_capacity,
    )


def pack_shm_header(
    layout: ShmLayout,
    *,
    world_input_length: int = 0,
    world_output_length: int = 0,
) -> bytes:
    """Encode the SHM file header for the given layout and lengths."""

    if world_input_length < 0:
        message = "world_input_length cannot be negative."
        raise ValueError(message)
    if world_output_length < 0:
        message = "world_output_length cannot be negative."
        raise ValueError(message)
    if world_input_length > layout.world_input_capacity:
        message = "world_input_length exceeds world_input_capacity."
        raise ValueError(message)
    if world_output_length > layout.world_output_capacity:
        message = "world_output_length exceeds world_output_capacity."
        raise ValueError(message)
    return struct.pack(
        SHM_HEADER_FMT,
        SHM_MAGIC,
        SHM_VERSION,
        layout.world_input_capacity,
        layout.world_output_capacity,
        world_input_length,
        world_output_length,
    )


def unpack_shm_header(
    header_bytes: bytes,
    *,
    fallback_layout: ShmLayout | None = None,
) -> tuple[ShmLayout, int, int]:
    """Decode the SHM header and fall back to the default layout if needed."""

    layout = fallback_layout or default_shm_layout()
    if len(header_bytes) < SHM_HEADER_SIZE:
        return layout, 0, 0
    (
        magic,
        version,
        world_input_capacity,
        world_output_capacity,
        world_input_length,
        world_output_length,
    ) = struct.unpack(  # noqa: E501
        SHM_HEADER_FMT,
        header_bytes[:SHM_HEADER_SIZE],
    )
    if magic != SHM_MAGIC or version != SHM_VERSION:
        return layout, 0, 0
    try:
        decoded_layout = ShmLayout(
            world_input_capacity=world_input_capacity,
            world_output_capacity=world_output_capacity,
        )
    except ValueError:
        return layout, 0, 0
    return decoded_layout, world_input_length, world_output_length
