from typing import Optional

import numpy as np

from ..base import BaseMessage
from ..standard.header import Header, AUTO

from .position import Position
from .quaternion import Quaternion


class Transformation(BaseMessage):
    header: Header = AUTO

    source: Optional[str]
    target: Optional[str]
    position: Position
    rotation: Quaternion

    @classmethod
    def from_pq(cls,
                pq: np.ndarray,
                source: Optional[str] = None,
                target: Optional[str] = None,
                header: Header = None) -> 'Transformation':
        p, q = pq[:3], pq[3:]
        return cls(
            header=header or Header(),
            source=source,
            target=target,
            position=Position.from_p(p),
            rotation=Quaternion.from_q(q),
        )
