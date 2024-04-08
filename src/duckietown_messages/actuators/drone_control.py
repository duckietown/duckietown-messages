from ..base import BaseMessage

class DroneControl(BaseMessage):
    """
    Roll Pitch Yaw(rate) Throttle Commands, simulating output from
    remote control. Values range from 1000 to 2000
    which corespond to values from 0% to 100%
    """
    roll: float
    pitch: float
    yaw: float
    throttle: float