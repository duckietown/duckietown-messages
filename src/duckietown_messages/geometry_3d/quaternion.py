import numpy as np

from ..base import BaseMessage
from ..standard.header import Header, AUTO


class Quaternion(BaseMessage):
    header: Header = AUTO

    w: float
    x: float
    y: float
    z: float

    @classmethod
    def from_q(cls, q: np.ndarray, header: Header = None) -> 'Quaternion':
        return cls(
            header=header or Header(),
            w=float(q[0]),
            x=float(q[1]),
            y=float(q[2]),
            z=float(q[3]),
        )
