#!/usr/bin/env python3
"""Test for tool arguments logging functionality."""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.manager import Manager

def test_tool_arguments_extraction():
    """Test the _get_tool_arguments method with different event structures."""
    manager = Manager()
    
    # Test case 1: Dictionary with arguments
    event_item_1 = {
        'name': 'test_tool',
        'arguments': '{"param1": "value1", "param2": "value2"}'
    }
    args_1 = manager._get_tool_arguments(event_item_1)
    print(f"Test 1 - Dictionary with arguments: {args_1}")
    assert args_1 == '{"param1": "value1", "param2": "value2"}'
    
    # Test case 2: Dictionary with long arguments (should be truncated)
    event_item_2 = {
        'name': 'test_tool',
        'arguments': '{"param1": "very_long_value_that_should_be_truncated", "param2": "another_long_value"}'
    }
    args_2 = manager._get_tool_arguments(event_item_2)
    print(f"Test 2 - Long arguments (should be truncated): {args_2}")
    assert args_2 == '{"param1": "very_long_value_that_should_be_truncated", "param2": "another_long_value"}'
    
    # Test case 3: Dictionary without arguments
    event_item_3 = {
        'name': 'test_tool'
    }
    args_3 = manager._get_tool_arguments(event_item_3)
    print(f"Test 3 - No arguments: {args_3}")
    assert args_3 == "no_args"
    
    # Test case 4: Nested structure
    event_item_4 = {
        'tool': {
            'name': 'test_tool',
            'arguments': '{"state": "has_enough_context"}'
        }
    }
    args_4 = manager._get_tool_arguments(event_item_4)
    print(f"Test 4 - Nested structure: {args_4}")
    assert args_4 == '{"state": "has_enough_context"}'
    
    print("✅ All tests passed!")

if __name__ == "__main__":
    test_tool_arguments_extraction() 