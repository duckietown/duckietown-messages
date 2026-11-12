from typing import Optional

from pydantic import Field

from duckietown_messages.actuators import CarLights, DifferentialPWM
from duckietown_messages.base import BaseMessage
from duckietown_messages.geometry_3d import Transformation
from duckietown_messages.standard import Boolean


class WorldEntityOutput(BaseMessage):
    differential_pwm: Optional[DifferentialPWM] = None
    car_lights: Optional[CarLights] = None
    state_reset_flag: Optional[Boolean] = None
    state_reset_pose: Optional[Transformation] = Field(
        None,
        description=(
            "Where a reset (state_reset_flag true) puts the entity, in the same frame and convention as "
            "the pose in WorldEntityInput; without it, a reset returns the entity to its initial pose"
        ),
    )
