# In this file we will test the json schema validation and its effect on the performance of the serialization and
# deserialization of the messages.

import logging
import timeit
import unittest

import warnings

import pydantic


warnings.filterwarnings("ignore")

logging.getLogger("nose2.plugins.loader.generators").setLevel(logging.INFO)
logging.getLogger("nose2.plugins.loader.parameters").setLevel(logging.INFO)
logging.getLogger("nose2.plugins.loader.discovery").setLevel(logging.INFO)
logging.getLogger("nose2.loader").setLevel(logging.INFO)

from duckietown_messages.base import BaseMessage

from typing import Optional


class Lvl3(BaseMessage):
    version: str = "1.0"
    frame: Optional[str] = None
    some_dict: Optional[dict] = None
    some_list: Optional[list] = None


class Lvl2(BaseMessage):
    lvl3: Lvl3


class Lvl1(BaseMessage):
    version: str = "1.0"
    frame: Optional[str] = None
    some_dict: Optional[dict] = None
    some_list: Optional[list] = None
    # nested
    lvl2: Lvl2


class TestValidationPerformance(unittest.TestCase):

    def test_data_validation__standard__header(self):
        good: dict = {
            "version": "1.1",
            "frame": "/frame1/",
            "some_dict": {
                "key1": "value1",
            },
            "some_list": [1, 2, 3],
            "lvl2": {
                "lvl3": {
                    "version": "1.2",
                    "frame": "/frame3/",
                    "some_dict": {
                        "key1": "value1",
                    },
                    "some_list": [1, 2, 3],
                }
            },
        }
        bad: dict = {
            "version": "1.1",
            "frame": "/frame1/",
            "some_dict": {
                "key1": "value1",
            },
            "some_list": [1, 2, 3],
            "lvl2": {
                "lvl3": {
                    "version": "1.2",
                    "frame": "/frame3/",
                    "some_dict": 3,
                    "some_list": [1, 2, 3],
                }
            },
        }
        Lvl1(**good)
        self.assertRaises(pydantic.ValidationError, Lvl1, **bad)

    def _benchmark(self, cls, good, bad, n=1000):
        # test good without validation
        t1 = timeit.timeit(lambda: cls(**good), number=n)
        # test good without validation
        t2 = timeit.timeit(lambda: cls(**bad), number=n)
        print(
            f"Benchmark for message '{cls.__module__}.{cls.__name__}':\n"
            f"    t1 [good]: {t1:.4f}s\n"
            f"    t2  [bad]: {t2:.4f}s\n"
        )

    def test_benchmark__standard__header(self):
        good: dict = {
            "version": "1.1",
            "frame": "/frame1/",
            "some_dict": {
                "key1": "value1",
            },
            "some_list": [1, 2, 3],
            "lvl2": {
                "lvl3": {
                    "version": "1.2",
                    "frame": "/frame3/",
                    "some_dict": {
                        "key1": "value1",
                    },
                    "some_list": [1, 2, 3],
                }
            },
        }
        bad: dict = {
            "version": "1.1",
            "frame": "/frame1/",
            "some_dict": {
                "key1": "value1",
            },
            "some_list": [1, 2, 3],
            "lvl2": {
                "lvl3": {
                    "version": "1.2",
                    "frame": "/frame3/",
                    "some_dict": 3,
                    "some_list": [1, 2, 3],
                }
            },
        }
        self._benchmark(Lvl1, good, bad, False)
