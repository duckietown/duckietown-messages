#!/usr/bin/env python3

import timeit
import cProfile
import pstats
import io
from pstats import SortKey

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from duckietown_messages.base import BaseMessage
from duckietown_messages.standard.header import Header
from duckietown_messages.sensors.image import Image
from duckietown_messages.geometry_3d.position import Position
import numpy as np

def test_header_creation():
    """Test Header creation performance"""
    header = Header()
    return header

def test_image_creation():
    """Test Image creation with large data"""
    # Create a 640x480 RGB image
    img_data = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
    img = Image.from_rgb(img_data)
    return img

def test_position_creation():
    """Test simple Position message creation"""
    pos = Position(x=1.0, y=2.0, z=3.0)
    return pos

def test_serialization():
    """Test serialization performance"""
    pos = Position(x=1.0, y=2.0, z=3.0)
    raw_data = pos.to_rawdata()
    return raw_data

def test_deserialization():
    """Test deserialization performance"""
    pos = Position(x=1.0, y=2.0, z=3.0)
    raw_data = pos.to_rawdata()
    pos_back = Position.from_rawdata(raw_data)
    return pos_back

def test_validation_heavy():
    """Test validation with complex nested structures"""
    from duckietown_messages_tests.benchmarks.test_performance import Lvl1
    
    data = {
        "version": "1.1",
        "frame": "/frame1/",
        "some_dict": {"key1": "value1"},
        "some_list": [1, 2, 3],
        "lvl2": {
            "lvl3": {
                "version": "1.2",
                "frame": "/frame3/",
                "some_dict": {"key1": "value1"},
                "some_list": [1, 2, 3],
            }
        },
    }
    msg = Lvl1(**data)
    return msg

def profile_function(func, name, iterations=1000):
    """Profile a function and print results"""
    print(f"\n=== Profiling {name} ({iterations} iterations) ===")
    
    # Time the function
    elapsed_time = timeit.timeit(func, number=iterations)
    print(f"Total time: {elapsed_time:.4f}s")
    print(f"Average per call: {elapsed_time/iterations*1000:.4f}ms")
    
    # Profile the function
    pr = cProfile.Profile()
    pr.enable()
    for _ in range(min(100, iterations)):  # Limit profiling iterations to avoid too much output
        func()
    pr.disable()
    
    # Print profiling results
    s = io.StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats(SortKey.CUMULATIVE)
    ps.print_stats(10)  # Print top 10 functions
    print(s.getvalue())

if __name__ == "__main__":
    print("Analyzing BaseMessage performance...")
    
    # Test basic operations
    profile_function(test_header_creation, "Header Creation", 10000)
    profile_function(test_position_creation, "Position Creation", 10000)
    profile_function(test_serialization, "Serialization", 1000)
    profile_function(test_deserialization, "Deserialization", 1000)
    profile_function(test_validation_heavy, "Complex Validation", 1000)
    
    # Test image creation (potentially CPU intensive)
    profile_function(test_image_creation, "Large Image Creation", 100)