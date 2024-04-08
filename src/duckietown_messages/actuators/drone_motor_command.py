from ..base import BaseMessage
from ..standard.header import AUTO, Header

class DroneMotorCommand(BaseMessage):
    """
    PWM commands from the range defined on betaflight for each motor.
    """
    header: Header = AUTO
    
    # range defined on cleanflight
    minimum : int
    maximum : int

    # PWM commands for the individual motors
    m1 : int
    m2 : int
    m3 : int
    m4 : int
