from duckietown_messages.simulation.shm_layout import (
    SHM_HEADER_SIZE,
    default_shm_layout,
    pack_shm_header,
    resize_shm_layout,
    unpack_shm_header,
)


def test_pack_unpack_header_roundtrip() -> None:
    layout = default_shm_layout()
    header = pack_shm_header(
        layout,
        world_input_length=123,
        world_output_length=45,
    )

    decoded_layout, world_input_length, world_output_length = unpack_shm_header(header)

    assert decoded_layout == layout
    assert world_input_length == 123
    assert world_output_length == 45


def test_resize_layout_grows_to_fit_runtime_payload() -> None:
    layout = default_shm_layout()

    resized = resize_shm_layout(
        layout,
        min_world_input_capacity=layout.world_input_capacity + 1,
        min_world_output_capacity=layout.world_output_capacity * 3,
    )

    assert resized.world_input_capacity == layout.world_input_capacity * 2
    assert resized.world_output_capacity == layout.world_output_capacity * 4


def test_unpack_invalid_header_falls_back_to_default() -> None:
    layout = default_shm_layout()

    decoded_layout, world_input_length, world_output_length = unpack_shm_header(
        b"\x00" * SHM_HEADER_SIZE, fallback_layout=layout
    )

    assert decoded_layout == layout
    assert world_input_length == 0
    assert world_output_length == 0
