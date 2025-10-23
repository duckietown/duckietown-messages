from typing import List

from pydantic import Field

from ..base import BaseMessage
from ..standard.header import Header, AUTO


class Homography(BaseMessage):
    # Use __slots__ for memory efficiency
    __slots__ = ()
    
    header: Header = AUTO

    data: List[float] = Field(description="Homography matrix (flattened)")
