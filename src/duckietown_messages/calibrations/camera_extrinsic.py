from typing import Dict

from pydantic import Field

from ..base import BaseMessage
from ..geometry_2d.homography import Homography
from ..standard.header import Header, AUTO


class CameraExtrinsicCalibration(BaseMessage):
    header: Header = AUTO

    homographies: Dict[str, Homography] = Field(description="Collection of known homography matrices for different "
                                                            "target reference frames")
