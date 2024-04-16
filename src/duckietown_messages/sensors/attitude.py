from pydantic import Field
from ..base import BaseMessage
from ..standard.header import Header, AUTO


class Attitude(BaseMessage):
    # header
    header: Header = AUTO

    # orientation in quaternion form
    x: float = Field(description="Quaternion x component", ge=-1, le=1)
    y: float = Field(description="Quaternion y component", ge=-1, le=1)
    z: float = Field(description="Quaternion z component", ge=-1, le=1)
    w: float = Field(description="Quaternion w component", ge=-1, le=1)