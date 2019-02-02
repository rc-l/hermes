import unittest
import sys
from django.test.utils import setup_test_environment
import pacioli.tests
from importlib import reload


def suiteFactory(
        *testcases,
        testSorter   = None,
        suiteMaker   = unittest.makeSuite,
        newTestSuite = unittest.TestSuite
    ):
    """
    make a test suite from test cases, or generate test suites from test cases.
    *testcases     = TestCase subclasses to work on
    testSorter     = sort tests using this function over sorting by line number
    suiteMaker     = should quack like unittest.makeSuite.
    newTestSuite   = should quack like unittest.TestSuite.
    """

    if testSorter is None:
        ln         = lambda f:    getattr(tc, f).__code__.co_firstlineno
        testSorter = lambda a, b: ln(a) - ln(b)

    test_suite = newTestSuite()
    for tc in testcases:
        test_suite.addTest(suiteMaker(tc, sortUsing=testSorter))

    return test_suite

def execute():
    '''
    Run this from django's manage.py shell to execute the tests
    '''
    reload(pacioli.tests)  # Reload to automatically pick up changes in the test script.
    setup_test_environment
    cases = suiteFactory(pacioli.tests.TestsSystem)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(cases)

if __name__ == '__main__':
    print("Execute this using manage.py shell")
    sys.exit(1)
