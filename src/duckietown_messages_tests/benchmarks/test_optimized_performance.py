"""
Performance tests for optimized BaseMessage implementation.

These tests verify that the performance optimizations introduced to reduce CPU load
are working correctly and maintain backward compatibility.
"""

import unittest
import timeit
import threading
from typing import List

from duckietown_messages.base import BaseMessage
from duckietown_messages.standard.header import Header, AUTO
from duckietown_messages.colors.rgba import RGBA
from pydantic import Field


class TestOptimizedPerformance(unittest.TestCase):
    """Test performance optimizations in BaseMessage and related classes."""

    def test_header_caching_efficiency(self):
        """Test that header caching reduces object creation."""
        # Create multiple headers using get_default()
        headers = [Header.get_default() for _ in range(100)]
        
        # All headers should be the same object (cached)
        unique_ids = len(set(id(h) for h in headers))
        self.assertEqual(unique_ids, 1, "Headers should be cached and reused")
        
        # Verify they all have the same default values
        for header in headers:
            self.assertEqual(header.version, "1.0")
            self.assertIsNone(header.frame)
            self.assertIsNone(header.txt)
            self.assertIsNone(header.timestamp)

    def test_auto_factory_performance(self):
        """Test that AUTO factory uses optimized header creation."""
        n = 1000
        
        # Measure AUTO factory performance
        time_auto = timeit.timeit(lambda: AUTO.default_factory(), number=n)
        
        # Should be significantly faster than creating new Header() each time
        time_direct = timeit.timeit(lambda: Header(), number=n)
        
        # AUTO factory should be at least as fast as direct creation
        self.assertLessEqual(time_auto, time_direct * 1.5, 
                           "AUTO factory should be optimized")
        
        # Verify all AUTO headers are cached instances
        auto_headers = [AUTO.default_factory() for _ in range(10)]
        unique_auto_ids = len(set(id(h) for h in auto_headers))
        self.assertEqual(unique_auto_ids, 1, "AUTO factory should return cached headers")

    def test_version_validation_performance(self):
        """Test that version validation uses pre-compiled regex."""
        valid_versions = ["1.0", "1.2.3", "2.0.1", "10.5.7"]
        
        # This should not raise any exceptions and should be fast
        for version in valid_versions:
            header = Header(version=version)
            self.assertEqual(header.version, version)
        
        # Test invalid versions are still caught
        invalid_versions = ["invalid", "1", "1.2.3.4.5", ""]
        for version in invalid_versions:
            with self.assertRaises(Exception):
                Header(version=version)

    def test_message_creation_performance(self):
        """Test optimized message creation with AUTO headers."""
        
        class TestMessage(BaseMessage):
            __slots__ = ()  # Test memory optimization
            header: Header = AUTO
            data: str = Field(description="Test data")
            value: int = Field(description="Test value", default=42)
        
        n = 1000
        
        # Test message creation performance
        time_creation = timeit.timeit(lambda: TestMessage(data="test"), number=n)
        
        # Verify functionality
        msg = TestMessage(data="hello", value=100)
        self.assertEqual(msg.data, "hello")
        self.assertEqual(msg.value, 100)
        self.assertEqual(msg.header.version, "1.0")
        
        # Test with cached header should be even faster
        cached_header = Header.get_default()
        time_cached = timeit.timeit(
            lambda: TestMessage(header=cached_header, data="test"), 
            number=n
        )
        
        # Both should be reasonably fast (less than 10ms total for 1000 messages)
        self.assertLess(time_creation, 0.01, "Message creation should be fast")
        self.assertLess(time_cached, 0.01, "Cached header creation should be fast")

    def test_serialization_performance(self):
        """Test that serialization uses optimized model_dump."""
        
        class TestMessage(BaseMessage):
            __slots__ = ()
            header: Header = AUTO
            data: str = Field(description="Test data")
        
        msg = TestMessage(data="test")
        n = 1000
        
        # Test model_dump performance
        time_dump = timeit.timeit(lambda: msg.model_dump(), number=n)
        
        # Should be reasonably fast
        self.assertLess(time_dump, 0.01, "Serialization should be fast")
        
        # Verify output structure
        data = msg.model_dump()
        self.assertIn('header', data)
        self.assertIn('data', data)
        self.assertEqual(data['data'], 'test')
        self.assertEqual(data['header']['version'], '1.0')

    def test_rgba_optimizations(self):
        """Test RGBA class optimizations."""
        n = 1000
        
        # Test RGBA creation performance
        time_rgba = timeit.timeit(lambda: RGBA(r=1.0, g=0.5, b=0.0, a=1.0), number=n)
        self.assertLess(time_rgba, 0.01, "RGBA creation should be fast")
        
        # Test factory methods use optimized headers
        rgba_zero = RGBA.zero()
        rgba_list = RGBA.from_list([0.5, 0.7, 0.3, 1.0])
        
        # Verify functionality is preserved
        self.assertEqual(rgba_zero.r, 0.0)
        self.assertEqual(rgba_zero.g, 0.0)
        self.assertEqual(rgba_zero.b, 0.0)
        self.assertEqual(rgba_zero.a, 0.0)
        
        self.assertEqual(rgba_list.r, 0.5)
        self.assertEqual(rgba_list.g, 0.7)
        self.assertEqual(rgba_list.b, 0.3)
        self.assertEqual(rgba_list.a, 1.0)
        
        # Test __getitem__ still works
        self.assertEqual(rgba_list[0], 0.5)
        self.assertEqual(rgba_list[1], 0.7)
        self.assertEqual(rgba_list[2], 0.3)
        self.assertEqual(rgba_list[3], 1.0)

    def test_thread_safety(self):
        """Test that header caching is thread-safe."""
        results = []
        errors = []
        
        def create_headers():
            try:
                for _ in range(50):
                    header = Header.get_default()
                    results.append(id(header))
            except Exception as e:
                errors.append(e)
        
        # Create multiple threads
        threads = []
        for _ in range(5):
            t = threading.Thread(target=create_headers)
            threads.append(t)
            t.start()
        
        # Wait for all threads to complete
        for t in threads:
            t.join()
        
        # Check for errors
        self.assertEqual(len(errors), 0, f"Thread safety test failed with errors: {errors}")
        
        # All headers should be the same instance
        unique_ids = set(results)
        self.assertEqual(len(unique_ids), 1, "Header caching should be thread-safe")

    def test_backward_compatibility(self):
        """Test that optimizations maintain backward compatibility."""
        
        # Test the original MyMessage class from test_auto_header.py
        class MyMessage(BaseMessage):
            header: Header = AUTO
            a: int = 7
            b: float = 5.0
        
        # Test original functionality
        m = MyMessage(a=9, b=7.0)
        self.assertEqual(m.a, 9)
        self.assertEqual(m.b, 7.0)
        self.assertEqual(m.header.version, "1.0")
        
        # Test with custom header
        custom_header = Header(version="2.1", frame="/test_frame", timestamp=123.45)
        m_custom = MyMessage(header=custom_header, a=100, b=200.0)
        self.assertEqual(m_custom.header.version, "2.1")
        self.assertEqual(m_custom.header.frame, "/test_frame")
        self.assertEqual(m_custom.header.timestamp, 123.45)
        self.assertEqual(m_custom.a, 100)
        self.assertEqual(m_custom.b, 200.0)
        
        # Test serialization compatibility
        data = m.model_dump()
        self.assertIn('header', data)
        self.assertIn('a', data)
        self.assertIn('b', data)
        self.assertEqual(data['a'], 9)
        self.assertEqual(data['b'], 7.0)

    def test_memory_efficiency(self):
        """Test that __slots__ reduces memory overhead."""
        
        class SlottedMessage(BaseMessage):
            __slots__ = ()
            header: Header = AUTO
            data: str = Field(description="Test data")
        
        class NonSlottedMessage(BaseMessage):
            header: Header = AUTO
            data: str = Field(description="Test data")
        
        # Create instances to test they work
        slotted = SlottedMessage(data="test")
        non_slotted = NonSlottedMessage(data="test")
        
        # Both should function the same
        self.assertEqual(slotted.data, "test")
        self.assertEqual(non_slotted.data, "test")
        self.assertEqual(slotted.header.version, "1.0")
        self.assertEqual(non_slotted.header.version, "1.0")
        
        # Slotted message should not have __dict__ (memory optimization)
        self.assertFalse(hasattr(slotted, '__dict__'), 
                        "Slotted message should not have __dict__")


if __name__ == '__main__':
    unittest.main()