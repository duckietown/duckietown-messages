from ..base import BaseMessage
from ..standard.header import Header, AUTO


class DifferentialPWM(BaseMessage):
    # header
    header: Header = AUTO

    # PWM signal magnitude between -1 and 1 for the left wheel
    left: float

    # PWM signal magnitude between -1 and 1 for the left wheel
    right: float
