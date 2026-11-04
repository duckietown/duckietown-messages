import typing
from abc import ABCMeta

from pydantic import BaseModel, ValidationError

from dtps_http import RawData
from duckietown_messages.utils.exceptions import DataDecodingError


class BaseMessage(BaseModel, metaclass=ABCMeta):

    # TODO: add a field for the header and remove it from the subclasses

    @classmethod
    def from_rawdata(cls, rd: RawData, allow_none: bool = False) -> 'BaseMessage':
        native: object = rd.get_as_native_object()
        if native is None:
            if allow_none:
                # noinspection PyTypeChecker
                return None
            raise DataDecodingError(f"Expected a dict-like object, received None instead")
        # ---
        data: dict = typing.cast(dict, native)
        try:
            # noinspection PyArgumentList
            return cls(**data)
        except ValidationError as e:
            raise DataDecodingError(f"Error while parsing {cls.__name__} from {rd}: {e}", e)

    def to_native(self) -> dict:
        return self.model_dump()

    def to_rawdata(self) -> RawData:
        native = self.to_native()
        return RawData.cbor_from_native_object(native)
