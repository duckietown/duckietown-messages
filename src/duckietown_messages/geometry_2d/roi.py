from ..base import BaseMessage
from ..standard.header import Header, AUTO


class ROI(BaseMessage):
    # header
    header: Header = AUTO

    # height of ROI
    height: int
    # width of ROI
    width: int

    # leftmost pixel of the ROI (0 if the ROI includes the left edge of the image)
    x: int = 0
    # topmost pixel of the ROI (0 if the ROI includes the top edge of the image)
    y: int = 0
