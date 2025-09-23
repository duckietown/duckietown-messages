import re
from typing import Optional
from threading import Lock

from pydantic import Field, field_validator

from ..base import BaseMessage

# Pre-compile regex pattern for version validation to avoid repeated compilation
_VERSION_PATTERN = re.compile(r"^[0-9]+\.[0-9]+(\.[0-9]+)?$")

# Header instance pool for reducing object creation overhead
class _HeaderPool:
    """Thread-safe header pool to reuse common header instances."""
    
    def __init__(self):
        self._lock = Lock()
        self._default_header = None
    
    def get_default_header(self) -> 'Header':
        """Get a default header instance, creating it only once."""
        if self._default_header is None:
            with self._lock:
                if self._default_header is None:
                    self._default_header = Header()
        return self._default_header

_header_pool = _HeaderPool()


class Header(BaseMessage):
    # Use __slots__ to reduce memory overhead
    __slots__ = ()
    
    # version of the message this header is attached to
    version: str = Field(
        description="Version of the message this header is attached to",
        examples=["0.1.3"],
        default="1.0"
    )
    # reference frame this data is captured in
    frame: Optional[str] = Field(description="Reference frame this data is captured in", default=None)
    # auxiliary data for the message
    txt: Optional[dict] = Field(description="Auxiliary data attached to the message", default=None)
    # timestamp
    timestamp: Optional[float] = Field(description="Timestamp", default=None)
    
    @field_validator('version')
    @classmethod
    def validate_version(cls, v: str) -> str:
        """Validate version using pre-compiled regex pattern."""
        if not _VERSION_PATTERN.match(v):
            raise ValueError(f"Version must match pattern: {_VERSION_PATTERN.pattern}")
        return v
    
    @classmethod
    def get_default(cls) -> 'Header':
        """Get a cached default header instance to reduce object creation."""
        return _header_pool.get_default_header()


def _create_optimized_header() -> Header:
    """Optimized header factory that may reuse instances for common cases."""
    return Header.get_default()


AUTO = Field(default_factory=_create_optimized_header, description="Auto-generated header")
