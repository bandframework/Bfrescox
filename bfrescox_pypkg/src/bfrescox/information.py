from pathlib import Path

from ._load_build_information import _load_build_information


def information():
    """
    All code that would like to use the |frescox| executable built for this
    package should use this information to obtain the absolute path to the
    executable to avoid the situation of simply calling |frescox| with no path
    and inadvertently using a different executable if, for example, the ``PATH``
    variable is mismanaged.

    .. note::
        **EXPERT USERS ONLY** An empty ``dict`` indicates a hollow |bfrescox|
        installation

    :return: ``dict`` that contains information regarding the |frescox|
        executable used by the package.
    """
    return _load_build_information(Path(__file__).resolve().parent)
