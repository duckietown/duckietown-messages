from ..base import BaseMessage
from ..standard.header import Header, AUTO


class Point(BaseMessage):
    header: Header = AUTO

    x: float
    y: float
