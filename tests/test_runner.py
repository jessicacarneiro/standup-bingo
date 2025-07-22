"""
Test runner and configuration for the bingo generator test suite.

This module provides utilities for running tests and can be executed
directly to run all tests in the test suite.
"""

import unittest
import sys
import os
from pathlib import Path

# Add the parent directory to the path so we can import bingo_generator
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def run_all_tests():
    """Run all tests in the test suite."""
    # Discover and run all tests in the tests directory
    loader = unittest.TestLoader()
    test_dir = Path(__file__).parent
    suite = loader.discover(test_dir, pattern='test_*.py')
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


def run_specific_test(test_name):
    """Run a specific test module or test case."""
    loader = unittest.TestLoader()
    
    try:
        # Try to load as a module first
        suite = loader.loadTestsFromName(test_name)
    except (ImportError, AttributeError):
        print(f"Could not find test: {test_name}")
        return False
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


def main():
    """Main entry point for the test runner."""
    if len(sys.argv) > 1:
        # Run specific test
        test_name = sys.argv[1]
        success = run_specific_test(test_name)
    else:
        # Run all tests
        success = run_all_tests()
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
