from typing import Optional

from duckietown_messages.base import BaseMessage
from duckietown_messages.standard import Header
from duckietown_messages.standard.header import AUTO

from .world_entity_input import WorldEntityInput


class WorldInput(BaseMessage):
    header: Header = AUTO
    session_id: Optional[int] = None
    entities: Optional[dict[str, WorldEntityInput]] = None
