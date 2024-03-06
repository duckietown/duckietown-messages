from ..base import BaseMessage
from ..standard.header import Header, AUTO


class LinearAccelerations(BaseMessage):
    # header
    header: Header = AUTO

    # linear acceleration along the 3 axis
    x: float
    y: float
    z: float
