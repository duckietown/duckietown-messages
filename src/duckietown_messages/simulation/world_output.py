from typing import Optional

from duckietown_messages.actuators import CarLights, DifferentialPWM
from duckietown_messages.base import BaseMessage
from duckietown_messages.standard import Boolean
from duckietown_messages.standard.header import AUTO, Header


class WorldOutput(BaseMessage):
    header: Header = AUTO
    differential_pwm: Optional[DifferentialPWM] = None
    car_lights: Optional[CarLights] = None
    state_reset_flag: Optional[Boolean] = None
