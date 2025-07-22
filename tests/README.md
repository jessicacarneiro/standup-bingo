# Test Configuration and Requirements

This directory contains the test suite for the Standup Bingo Card Generator.

## Test Structure

- `test_bingo_generator.py` - Main functionality tests
- `test_edge_cases.py` - Edge cases and error handling tests  
- `test_runner.py` - Test runner utilities
- `__init__.py` - Test package initialization

## Running Tests

### Run All Tests
```bash
# From the project root directory
python -m pytest tests/

# Or using unittest
python -m unittest discover tests/

# Or using the custom test runner
python tests/test_runner.py
```

### Run Specific Test Files
```bash
# Run main functionality tests
python -m unittest tests.test_bingo_generator

# Run edge case tests
python -m unittest tests.test_edge_cases
```

### Run Specific Test Classes
```bash
# Run specific test class
python -m unittest tests.test_bingo_generator.TestBingoGenerator

# Run specific test method
python -m unittest tests.test_bingo_generator.TestBingoGenerator.test_read_entries_valid_file
```

## Test Coverage

The test suite covers:

### Core Functionality
- ✅ Reading entries from files
- ✅ Generating random bingo cards
- ✅ PDF generation (mocked)
- ✅ Command-line interface
- ✅ End-to-end workflow

### Edge Cases
- ✅ Empty files and entries
- ✅ Unicode and special characters
- ✅ Large files
- ✅ Invalid inputs
- ✅ File permission errors
- ✅ Boundary conditions

### Error Handling
- ✅ Missing files
- ✅ Invalid arguments
- ✅ Insufficient entries
- ✅ Permission errors

## Test Dependencies

The tests use Python's built-in `unittest` framework and require no additional dependencies beyond what the main application uses.

## Continuous Integration

These tests are designed to be run in CI/CD pipelines. The test runner returns appropriate exit codes:
- 0: All tests passed
- 1: One or more tests failed

## Adding New Tests

When adding new functionality to the bingo generator:

1. Add tests to the appropriate test file
2. Follow the existing naming conventions
3. Include both positive and negative test cases
4. Add docstrings explaining what each test validates
5. Update this README if adding new test files

## Test Data

Tests create temporary files and directories during execution and clean up automatically. No persistent test data is required.
