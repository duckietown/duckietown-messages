from typing import List

from duckietown_messages.base import BaseMessage
from duckietown_messages.standard.header import Header, AUTO


class RGBA(BaseMessage):
    header: Header = AUTO

    # intensities of the red, green, and blue components of the color in the range [0, 1]
    r: float
    g: float
    b: float

    # alpha channel in the range [0, 1]
    a: float

    def __getitem__(self, item):
        return [self.r, self.g, self.b, self.a][item]

    @classmethod
    def zero(cls, header: Header = None) -> 'RGBA':
        return cls(
            header=header or Header(),
            r=0,
            g=0,
            b=0,
            a=0,
        )

    @classmethod
    def from_list(cls, lst: List[float], header: Header = None) -> 'RGB':
        assert len(lst) == 4
        return cls(
            header=header or Header(),
            r=lst[0],
            g=lst[1],
            b=lst[2],
            a=lst[3],
        )
