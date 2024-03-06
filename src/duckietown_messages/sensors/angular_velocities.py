from ..base import BaseMessage
from ..standard.header import Header, AUTO


class AngularVelocities(BaseMessage):
    # header
    header: Header = AUTO

    # angular acceleration about the 3 axis
    x: float
    y: float
    z: float
