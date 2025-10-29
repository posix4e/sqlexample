#!/usr/bin/env python3
"""
Test SQL Parser with Example Queries

This script tests the SQL parser against valid and invalid example queries.
Valid queries should parse successfully, invalid queries should fail.
"""

import os
import sys
from pathlib import Path
from collections import defaultdict


def test_queries():
    """Test all example queries and report results."""

    # First, ensure the parser is generated
    print("=" * 80)
    print("Generating SQL Parser...")
    print("=" * 80)

    import subprocess
    result = subprocess.run(
        [sys.executable, "generate_parser.py"],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print("Error generating parser:", file=sys.stderr)
        print(result.stderr, file=sys.stderr)
        return False

    print("✓ Parser generated successfully\n")

    # Import the generated parser
    try:
        from sql_parser import SQLParser
    except ImportError as e:
        print(f"Error importing parser: {e}", file=sys.stderr)
        print("Make sure lark-parser is installed: pip install lark-parser", file=sys.stderr)
        return False

    parser = SQLParser()

    # Test valid queries
    print("=" * 80)
    print("Testing Valid Queries")
    print("=" * 80)

    valid_dir = Path("examples/queries/valid")
    valid_files = sorted(valid_dir.glob("*.sql"))

    valid_passed = 0
    valid_failed = 0
    valid_errors = []

    for query_file in valid_files:
        with open(query_file, 'r') as f:
            sql = f.read()

        try:
            parser.parse(sql)
            print(f"✓ {query_file.name}")
            valid_passed += 1
        except Exception as e:
            print(f"✗ {query_file.name}")
            print(f"  Error: {e}")
            valid_failed += 1
            valid_errors.append((query_file.name, str(e)))

    print()
    print(f"Valid Queries: {valid_passed} passed, {valid_failed} failed")
    print()

    # Test invalid queries
    print("=" * 80)
    print("Testing Invalid Queries")
    print("=" * 80)

    invalid_dir = Path("examples/queries/invalid")
    invalid_files = sorted(invalid_dir.glob("*.sql"))

    invalid_passed = 0
    invalid_failed = 0
    invalid_errors = []

    for query_file in invalid_files:
        with open(query_file, 'r') as f:
            sql = f.read()

        try:
            parser.parse(sql)
            print(f"✗ {query_file.name} - Should have failed but parsed successfully!")
            invalid_failed += 1
            invalid_errors.append((query_file.name, "Parsed successfully when it should have failed"))
        except Exception as e:
            print(f"✓ {query_file.name} - Failed as expected")
            invalid_passed += 1

    print()
    print(f"Invalid Queries: {invalid_passed} failed as expected, {invalid_failed} incorrectly parsed")
    print()

    # Summary
    print("=" * 80)
    print("Summary")
    print("=" * 80)
    print(f"Valid queries:   {valid_passed}/{len(valid_files)} passed")
    print(f"Invalid queries: {invalid_passed}/{len(invalid_files)} failed as expected")
    print()

    total_tests = len(valid_files) + len(invalid_files)
    total_passed = valid_passed + invalid_passed

    print(f"Total: {total_passed}/{total_tests} tests passed")
    print("=" * 80)

    # Show errors if any
    if valid_errors:
        print()
        print("Valid Query Errors:")
        print("-" * 80)
        for filename, error in valid_errors:
            print(f"\n{filename}:")
            print(f"  {error}")

    if invalid_errors:
        print()
        print("Invalid Query Errors (should not have parsed):")
        print("-" * 80)
        for filename, error in invalid_errors:
            print(f"\n{filename}:")
            print(f"  {error}")

    # Return success if all tests passed
    success = (valid_failed == 0 and invalid_failed == 0)

    if success:
        print()
        print("✓ All tests passed!")
        print()
    else:
        print()
        print("✗ Some tests failed")
        print()

    return success


if __name__ == "__main__":
    success = test_queries()
    sys.exit(0 if success else 1)
