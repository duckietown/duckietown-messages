from typing import Optional

from ....base import BaseMessage
from ....network.dtps.context import DTPSContextMsg


class HILConnectionConfiguration(BaseMessage):
    # source
    source: Optional[DTPSContextMsg]

    # agent information
    agent_name: str

    def __str__(self):
        return "HILConnectionConfiguration(source=%s, agent_name=%r,)" % (self.source, self.agent_name)
