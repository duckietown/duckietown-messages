from typing import List, Union

from .context import DTPSContextMsg
from ...base import BaseMessage


class DTPSPassthroughConnection(BaseMessage):
    # source
    source: DTPSContextMsg

    # paths
    paths: Union[List[str], None] = None

    def __str__(self):
        return "DTPSPassthroughConnection(source=%s, paths=%r,)" % (self.source, self.paths)
