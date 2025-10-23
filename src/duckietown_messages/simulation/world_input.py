from typing import Optional

from duckietown_messages.base import BaseMessage
from duckietown_messages.geometry_3d import Transformation, Twist
from duckietown_messages.sensors import Camera, CompressedImage, Imu, Range
from duckietown_messages.standard import Header, Integer
from duckietown_messages.standard.header import AUTO


class WorldInput(BaseMessage):
    header: Header = AUTO
    pose: Optional[Transformation] = None
    twist: Optional[Twist] = None
    compressed_image: Optional[CompressedImage] = None
    camera: Optional[Camera] = None
    tof_ranges: Optional[dict[str, Range]] = None
    imus: Optional[dict[str, Imu]] = None
    left_encoder_ticks: Optional[Integer] = None
    right_encoder_ticks: Optional[Integer] = None
