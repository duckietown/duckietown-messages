from typing import Union, List

from ...base import BaseMessage


class DTPSContextMsg(BaseMessage):
    # context configuration
    name: str
    urls: Union[List[str], None] = None
    path: Union[str, None] = None

    def __str__(self):
        return "DTPSContextMsg(name=%r, urls=%r, path=%r)" % (self.name, self.urls, self.path)
