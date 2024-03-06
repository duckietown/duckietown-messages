from ...base import BaseMessage
from ...standard.header import Header, AUTO


class HILConnectionConfiguration(BaseMessage):
    # header
    header: Header = AUTO

    # connection configuration
    engine_url: str | None
    agent_name: str | None
    agent_configuration: str | None
    dreamwalking: bool = False
