"""
Test module.

Runs all tests.
"""

import unittest

def main():

    _run_test_suite('testing/unittests', '*test.py')
    _run_test_suite('testing/functionaltests', '*test.py')

def _run_test_suite(directory, pattern):

    loader = unittest.TestLoader()
    runner = unittest.TextTestRunner(verbosity=2)
    suite = loader.discover(directory, pattern)

    runner.run(suite)

if __name__ == '__main__':

    main()
