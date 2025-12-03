from pydantic import Field

from duckietown_messages.base import BaseMessage
from duckietown_messages.standard.header import Header, AUTO


class String(BaseMessage):
    header: Header = AUTO

    data: str = Field(description="String payload")
