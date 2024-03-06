import unittest

from duckietown_messages.base import BaseMessage
from duckietown_messages.standard.header import Header, AUTO


class MyMessage(BaseMessage):
    header: Header = AUTO
    a: int = 7
    b: float = 5.0


class TestAutoHeader(unittest.TestCase):

    def test_auto_header(self):
        m = MyMessage(a=9, b=7.0)
        print(m)
