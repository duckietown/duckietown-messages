import typing
from abc import ABCMeta

from pydantic import BaseModel, ValidationError

from dtps_http import RawData
from duckietown_messages.utils.exceptions import DataDecodingError


class BaseMessage(BaseModel, metaclass=ABCMeta):

    @classmethod
    def from_rawdata(cls, rd: RawData) -> 'BaseMessage':
        data: dict = typing.cast(dict, rd.get_as_native_object())
        try:
            # noinspection PyArgumentList
            return cls(**data)
        except ValidationError as e:
            raise DataDecodingError(f"Error while parsing {cls.__name__} from {rd}: {e}", e)

    def to_rawdata(self) -> RawData:
        return RawData.cbor_from_native_object(self.dict())
