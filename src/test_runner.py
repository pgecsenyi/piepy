"""
Runs all tests.
"""

import sys
import unittest

def main():

    exit_code = 0
    test_result = run_test_suite('testing', '*test.py')

    if test_result.errors or test_result.failures:
        exit_code = 1

    sys.exit(exit_code)

def run_test_suite(directory, pattern):

    loader = unittest.TestLoader()
    runner = unittest.TextTestRunner(verbosity=2)
    suite = loader.discover(directory, pattern)

    return runner.run(suite)

if __name__ == '__main__':

    main()
