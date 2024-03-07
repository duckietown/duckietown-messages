from ..base import BaseMessage
from ..colors.rgba import RGBA
from ..standard.header import Header, AUTO


class CarLights(BaseMessage):
    # header
    header: Header = AUTO

    # lights
    front_left: RGBA
    front_right: RGBA
    rear_left: RGBA
    rear_right: RGBA
