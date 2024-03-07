from typing import Optional

from dt_computer_vision.camera import CameraModel
from ..base import BaseMessage
from ..standard.header import Header, AUTO


class Camera(BaseMessage):
    # header
    header: Header = AUTO

    width: int
    height: int
    K: list
    D: list
    P: list
    R: Optional[list] = None
    H: Optional[list] = None

    @classmethod
    def from_camera_model(cls, camera: CameraModel, header: Header = None) -> 'Camera':
        return Camera(
            header=header or Header(),
            width=camera.width,
            height=camera.height,
            K=camera.K.tolist(),
            D=camera.D.tolist(),
            P=camera.P.tolist(),
            R=camera.R.tolist() if camera.R is not None else None,
            H=camera.H.tolist() if camera.H is not None else None,
        )
