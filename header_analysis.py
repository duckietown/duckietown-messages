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
from duckietown_messages.standard.header import Header, AUTO
from duckietown_messages.geometry_3d.position import Position

def test_direct_header():
    """Test creating Position with explicit header"""
    header = Header()
    pos = Position(header=header, x=1.0, y=2.0, z=3.0)
    return pos

def test_auto_header():
    """Test creating Position with AUTO header (default_factory)"""
    pos = Position(x=1.0, y=2.0, z=3.0)
    return pos

def test_no_header():
    """Test creating Position without header at all"""
    pos = Position(x=1.0, y=2.0, z=3.0)
    return pos

def test_header_regex_validation():
    """Test the regex validation that might be slow"""
    # This should trigger validation of the version pattern
    header = Header(version="1.2.3")
    return header

def test_bad_header_regex():
    """Test invalid version format that would fail validation"""
    try:
        header = Header(version="invalid_version")
        return header
    except Exception as e:
        return e

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
    for _ in range(min(100, iterations)):
        func()
    pr.disable()
    
    # Print profiling results
    s = io.StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats(SortKey.CUMULATIVE)
    ps.print_stats(15)  # Print top 15 functions
    print(s.getvalue())

if __name__ == "__main__":
    print("Analyzing Header and AUTO performance...")
    
    # Test header operations
    profile_function(test_direct_header, "Direct Header Creation", 5000)
    profile_function(test_auto_header, "AUTO Header Creation", 5000)
    profile_function(test_header_regex_validation, "Header Regex Validation", 5000)
    
    # Test validation failures
    profile_function(test_bad_header_regex, "Bad Header Validation", 1000)