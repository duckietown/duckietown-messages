from typing import Optional

from pydantic import Field

from ..base import BaseMessage


class Header(BaseMessage):
    # version of the message this header is attached to
    version: str = "1.0"
    # reference frame this data is captured in
    frame: Optional[str] = None
    # auxiliary data for the message
    txt: Optional[dict] = None


AUTO = Field(default_factory=Header, description="Auto-generated header")
