from ..base import BaseMessage
from ..standard.header import Header, AUTO


class RangeFinder(BaseMessage):
    # header
    header: Header = AUTO

    # the size of the arc that the distance reading is valid for in randians. 0 corresponds to the x-axis of the sensor.
    fov: float

    # minimum range value (meters)
    minimum: float

    # maximum range value (meters)
    maximum: float
