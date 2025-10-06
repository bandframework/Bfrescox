Getting Started
===============

The |bfrescox| package is capable of building, installing, and using a |frescox|
executable on macOS- and Linux-based systems.  Our test suite presently checks
builds with both macOS and Ubuntu.  We expect that it would work with other
similar Linux operating systems.

General Installations
---------------------
While we intend for this package to eventually be distributed by PyPI for direct
installation |via| |pip|, during this alpha development phase, users must
install the package directly from a local clone of the |bfrescox| repository.
For developer installations, refer to the :numref:`tox_usage:Developer
Environment`.

Dependencies
^^^^^^^^^^^^
Building |frescox| requires the installation of a known compiler suite including
a Fortran compiler.  At present, installations require either the use of the

* GCC compiler suite (``gfortran``) or
* an Intel compiler suite (``ifort`` or ``ifx``).

Installation from local clone
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. _`Bfrescox clone`: https://github.com/bandframework/Bfrescox

After installing a local `Bfrescox clone`_ and setting up your target Python
environment as desired, execute

.. code-block:: console

    $ cd /path/to/Bfrescox/bfrescox_pypkg
    $ python -m pip install .

Testing
-------
The |bfrescox| Python package has an automated test suite integrated in the
package that can be run to test an installation.  After installing the package,
the installation can be tested by executing

.. code-block:: console

    $ python
    >>> import bfrescox
    >>> bfrescox.__version__
    <version>
    >>> bfrescox.test()
        ...
