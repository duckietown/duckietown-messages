from ..base import BaseMessage
from ..standard.header import Header, AUTO


class Attitude(BaseMessage):
    # header
    header: Header = AUTO

    # angular acceleration about the 3 axis
    roll: float
    pitch: float
    yaw: float