import numpy as np

from ..base import BaseMessage
from ..standard.header import Header, AUTO


class Position(BaseMessage):
    header: Header = AUTO

    x: float
    y: float
    z: float

    @classmethod
    def from_p(cls, p: np.ndarray, header: Header = None) -> 'Position':
        return cls(
            header=header or Header(),
            x=float(p[0]),
            y=float(p[1]),
            z=float(p[2]),
        )
