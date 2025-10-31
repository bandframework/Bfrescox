|bfrescox| Python package
=========================

|bfrescox| is a Python package wrapping |frescox|:cite:t:`thompson1988coupled`,
a Fortran library for coupled-reaction-channels calculations in nuclear physics.
The intention of this package is to provide a user-friendly experience to
perform parametric reaction calculations and uncertainty quantification studies
with |frescox|.

|frescox| is available `on github <https://github.com/llnl/frescox>`_, and also
has a `dedicated website <https://www.fresco.org.uk/index.htm>`_. The |bfrescox|
build system automatically downloads and compiles |frescox| as part of its
installation process, and provides an interface to build input configurations
for |frescox|, run calculations, and parse output results.

|bfrescoxpro| is a sister package to |bfrescox| that provides a similar
interface, with more options available for setting up the |frescox|
installation, including support for MPI and OpenMP builds.

These packages are being developed as part of |band| |via| collaboration.

.. note::

    |bfrescox| and |bfrescoxpro| are offered under the BSD-2-Clause license. By
    using these packages, you agree to the terms of this license.

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
   contributing_templates
   api
   advanced_users
   bibliography

.. toctree::
   :numbered:
   :maxdepth: 1
   :caption: Developer Guide:

   contributing
   tox_usage
