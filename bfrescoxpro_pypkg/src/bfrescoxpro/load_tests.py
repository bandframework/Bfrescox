from pathlib import Path


def load_tests(loader, *_):
    """
    This function implements the ``load_tests`` protocol of the Python
    ``unittest`` package so that clients using the package don't need to know
    where the tests are or what patterns they need to look for to find all
    tests.

    Developers and users can run tests using this indirectly |via|::

                       python -m unittest bfrescoxpro

    :param loader: ``unittest.TestLoader`` instance doing the loading
    :return: ``unittest`` test suite that contains all tests to be run to
        check correctness of all code in the overall package
    """
    here_dir = Path(__file__).resolve().parent
    start_dir = here_dir.joinpath("tests")

    return loader.discover(
        start_dir=str(start_dir),
        top_level_dir=str(here_dir),
        pattern="Test*.py"
    )
