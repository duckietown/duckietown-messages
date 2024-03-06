import typing
from abc import ABCMeta

from pydantic import BaseModel

from dtps_http import RawData


class BaseMessage(BaseModel, metaclass=ABCMeta):

    @classmethod
    def from_rawdata(cls, rd: RawData) -> 'BaseMessage':
        data: dict = typing.cast(dict, rd.get_as_native_object())
        # noinspection PyArgumentList
        return cls(**data)

    def to_rawdata(self) -> RawData:
        return RawData.cbor_from_native_object(self.dict())
