from pathlib import Path
from unittest import TestLoader, TestSuite


def load_tests(loader: TestLoader, *_) -> TestSuite:
    """
    This function implements the ``load_tests`` protocol of the Python
    ``unittest`` package so that clients using the package don't need to
    know where the tests are or what patterns they need to look for to
    find all tests.

    Developers and users can run tests using this indirectly |via|::

                         python -m unittest bfrescox

    Parameters:
        loader: ``unittest.TestLoader`` instance doing the loading

    Returns:
        TestSuite: The loaded test suite
    """
    here_dir = Path(__file__).resolve().parent
    start_dir = here_dir.joinpath("tests")

    return loader.discover(
        start_dir=str(start_dir),
        top_level_dir=str(here_dir),
        pattern="Test*.py",
    )
