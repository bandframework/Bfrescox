Developer Environment
=====================
.. _tox: https://tox.wiki/en/latest/index.html

Developers are free to setup whatever environment that they may need to
facilitate their work.  However, each of the Python packages in the repository
includes a `tox`_ setup, which developers can also use to automatically setup
and manage dedicated venvs for different predefined development tasks.

Development with |tox|
----------------------

The following is a rough guide to help install |tox| as a command line tool in a
dedicated, minimal virtual environment and is based on a `webinar
<https://www.youtube.com/watch?v=PrAyvH-tm8E>`_ by Oliver Bestwalter.  His
solution is nice since |tox| is made available with no need to manually activate
its virtual environment.

.. note::
    Developers that would like to use |tox| should, at the very least, learn
    enough about it that they understand the difference between running ``tox``
    and ``tox -r``.

To create a Python virtual environment that solely hosts |tox|, execute some
variation of the following using the desired target Python

.. code-block:: console

    $ cd $HOME/local/venv
    $ deactivate (to deactivate the current virtual environment if you are in one)
    $ /path/to/desired/python --version
    $ /path/to/desired/python -m venv $HOME/local/venv/.toxbase
    $ ./.toxbase/bin/python -m pip list
    $ ./.toxbase/bin/python -m pip install --upgrade pip setuptools (if installed)
    $ ./.toxbase/bin/python -m pip install tox
    $ ./.toxbase/bin/python -m pip list
    $ ./.toxbase/bin/tox --version

To avoid having to activate ``.toxbase`` every time we would like to work with
|tox|, we setup |tox| in ``PATH``.  Note that developers can use this single
|tox| installation for multiple projects.  Please replace ``.bash_profile`` with
the appropriate shell configuration file and tailor the following to your needs.

.. code-block:: console

    $ mkdir $HOME/local/bin
    $ ln -s $HOME/local/venv/.toxbase/bin/tox $HOME/local/bin/tox
    $ vi $HOME/.bash_profile (add $HOME/local/bin to PATH)
    $ . $HOME/.bash_profile
    $ which tox
    $ tox --version


No work will be carried out by default with the calls ``tox`` and ``tox -r``.

The following tasks can be run from within the directory hierarchy that contains
the package's |tox| configuration file

.. code-block:: console

    /path/to/bfrescox_pypkg/tox.ini

* ``tox -r -e coverage``

  * Execute the full test suite for the package and save coverage results to
    the coverage file
  * The test runs the package code in the local clone rather than code
    installed into Python so that coverage results accessed through web
    services such as CodeCov are clean and straightforward
  * If the environment variable ``COVERAGE_FILE`` is set, then this is the
    coverage file that will be written to.  If it is not specified, then the
    coverage results are written to ``.coverage_bfrescox`` for |bfrescox| or
    ``.coverage_bfrescoxpro`` for |bfrescoxpro|.

* ``tox -r -e nocoverage``

  * Execute the full test suite for the package using the code installed into
    Python

* ``tox -r -e report``

  * It is intended that this be run after or with ``coverage``
  * Display a code coverage report for the package's full test suite and
    generate XML and HTML versions of the report
  * For both packages, the environment variables ``COVERAGE_XML``
    and ``COVERAGE_HTML`` can be provided to specify the names of the files that
    the associated reports should be written to.  If ``COVERAGE_XML`` is not
    specified, then the XML report is written to ``coverage.xml``.  If
    ``COVERAGE_HTML`` is not provided, then the HTML report is written to
    ``htmlcov``.

* ``tox -r -e check``

  * Run several checks on the code to report possible issues
  * No files are altered automatically by this task

* ``tox -r -e html`` (|bfrescox| only)

  * Generate and render documentation locally in HTML

* ``tox -r -e pdf`` (|bfrescox| only)

  * Generate and render the documentation locally as a PDF file
  * Users are responsible for installing ``make`` and a compatible LaTeX
    installation for immediate use by |tox|.

* ``tox -e book`` (|bfrescox| only)

    * Generate from scratch in ``book/_build`` the |bfrescox| examples
      Jupyter book

Additionally, you can run any combination of the above such as ``tox -r -e
report,coverage``.

Direct use of |tox| venvs
-------------------------
Many of the tox tasks will build their |bfrescox| or |bfrescoxpro| binary
automatically each time they are run, which can significantly slow development
work.  In such cases, a developer will likely start their work by creating a
clean virtual environment for their task using ``tox -r`` and subsequently load
and work in that venv directly.

Developer's can inspect ``tox.ini`` to see what commands are run by their task
and adapt these for their work.

The following example shows how to run only a single test case using the
``coverage`` virtual environment setup by |tox|.

.. code-block:: console

    $ cd /path/to/bfrescox_pypkg
    $ tox -r -e coverage
    $ . ./.tox/coverage/bin/activate
    $ which python
    $ python --version
    $ python -m pip list
    $ python -m unittest bfrescox.tests.TestConfiguration

Note that using the ``coverage`` venv directly can be particularly useful since
the package is installed in editable mode and therefore facilitates interactive
development and testing of the Python code.
