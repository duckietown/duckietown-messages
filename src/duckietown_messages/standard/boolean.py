from duckietown_messages.base import BaseMessage
from duckietown_messages.standard.header import Header, AUTO


class Boolean(BaseMessage):
    header: Header = AUTO

    data: bool
