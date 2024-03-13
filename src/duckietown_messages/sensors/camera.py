from typing import Optional

from ..base import BaseMessage
from ..standard.header import Header, AUTO


class Camera(BaseMessage):
    # header
    header: Header = AUTO

    width: int
    height: int
    K: list
    D: list
    P: list
    R: Optional[list] = None
    H: Optional[list] = None
