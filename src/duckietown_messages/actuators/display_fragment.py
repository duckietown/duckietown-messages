import numpy as np

from ..base import BaseMessage
from ..sensors.image import Image
from ..standard.header import Header, AUTO
from ..geometry_2d.roi import ROI


class DisplayFragment(BaseMessage):
    # header
    header: Header = AUTO

    # ID of the fragment, used to update fragments that repeat over time
    name: str

    # display region this fragment should be rendered on
    region: int

    # page this fragment should be rendered on
    page: int

    # fragment content
    content: Image

    # location on the display where to show the fragment
    location: ROI

    # z-index of the fragment
    z: int

    # Time-to-Live in seconds of the fragment (-1 for infinite, do not abuse)
    ttl: int

    @property
    def as_mono8(self) -> np.ndarray:
        # validate encoding
        assert self.content.encoding in ["mono1", "mono8"]
        # make a copy
        im = self.content.data.copy()
        # turn mono1 into mono8
        if self.encoding == "mono1":
            im *= 255
        # ---
        return im
