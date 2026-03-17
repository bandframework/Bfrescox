|bfrescox| Python package
=========================

|bfrescox| is a Python package wrapping |frescox| :cite:t:`thompson1988coupled`,
a Fortran library for coupled-reaction-channels calculations in nuclear physics.
The intention of this package is to provide a user-friendly experience to
perform parametric reaction calculations and uncertainty quantification studies
with a |frescox| executable that is built from the code in the |frescox|
repository and installed automatically in |bfrescox| during |bfrescox|
installation.

|frescox| is available `on github <https://github.com/llnl/frescox>`_, and also
has a `dedicated website <https://www.fresco.org.uk/index.htm>`_. The |bfrescox|
build system automatically downloads and compiles |frescox| as part of its
installation process, and provides an interface to build input configurations
for |frescox|, run calculations, and parse output results.

|bfrescoxpro| is a sister package to |bfrescox| that provides a similar
interface, with more options available for setting up the |frescox|
installation, including support for MPI and OpenMP builds.

These packages are being developed as part of |band| `framework
<https://bandframework.github.io/>`_.

.. note::


    By using the |bfrescox| and |bfrescoxpro| packages, you agree to the terms
    specified in the Bfrescox license.


.. note::

    This is presently being developed as an alpha version.  While all
    functionality offered officially is under test, the code and test suite are
    still under active development.  In addition, the interface of the package
    will likely undergo significant changes as we work to the first official
    release.

.. toctree::
   :numbered:
   :maxdepth: 1
   :caption: User Guide:

   get_started
   templates
   examples
   api
   advanced_users
   bibliography

.. toctree::
   :numbered:
   :maxdepth: 1
   :caption: Developer Guide:

   contributing
   tox_usage
