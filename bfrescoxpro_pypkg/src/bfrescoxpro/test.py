import unittest

from bfrescoxpro import load_tests


def test(verbosity: int = 1):
    """
    Run the full set of tests in the package with results presented to
    caller using a simple text interface.

    This is included so that users can test their actual installation
    directly or record test results in Jupyter notebook output for
    reproducibility |via|::

                            bfrescoxpro.test()

    Parameters:
        verbosity: int
            verbosity level to pass to the ``unittest`` ``TestRunner``
    Returns:
        bool
            True if all tests in package passed; False, otherwise.
    """
    loader = unittest.TestLoader()
    suite = load_tests(loader, None, None)
    result = unittest.TextTestRunner(verbosity=verbosity).run(suite)

    return result.wasSuccessful()
