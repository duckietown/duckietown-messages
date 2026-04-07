from typing import Optional

from duckietown_messages.base import BaseMessage
from duckietown_messages.standard.header import AUTO, Header

from .world_entity_output import WorldEntityOutput


class WorldOutput(BaseMessage):
    header: Header = AUTO
    session_id: Optional[int] = None
    entities: Optional[dict[str, WorldEntityOutput]] = None
