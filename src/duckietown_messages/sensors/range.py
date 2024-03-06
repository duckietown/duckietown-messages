from ..base import BaseMessage
from ..standard.header import Header, AUTO


class Range(BaseMessage):
    # header
    header: Header = AUTO

    # measured distance (meters, null if out-of-range)
    data: float | None
