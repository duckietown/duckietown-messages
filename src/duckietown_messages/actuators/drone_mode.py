from enum import IntEnum
from ..base import BaseMessage

class Mode(IntEnum):
    DISARMED = 0
    ARMED = 1
    FLYING = 2

class DroneModeMsg(BaseMessage):
    mode: Mode
    
class DroneModeResponse(BaseMessage):
    previous_mode: Mode
    current_mode: Mode