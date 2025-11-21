Advanced Users
==============

|bfrescoxpro|
-------------

The |bfrescoxpro| Python package is designed to be as similar to the |bfrescox|
package as possible while still allowing users to install the |bfrescoxpro|
package with a custom build of the package's |frescox| binary.  At present,
users can specify that the package build its binary with

* MPI distributed parallelism,
* OpenMP shared parallelism, or
* MPI+OpenMP hybrid parallelism.

The package and its distribution scheme have been designed to allow users to
build and use custom binaries on machines ranging from laptops to leadership
class machines that have MPI implementations provided and optimized by experts
for each particular machine.

This customization, however, requires that the |bfrescoxpro| package be
distributed as a source distribution.  Since users are required to install the
package and have the package build its |frescox| binary from scratch, they are
also responsible for setting up the software stack needed to build and use their
custom |frescox| binary before installing |bfrescoxpro| and every time that they
use the package's installation.  The extra thought and care required to use this
customization is one motivation for providing build customization through a
separate package with a different name.

Note that while |bfrescoxpro| might be needed to acquire data, the |bfrescox|
package can be used on any machine to load and analyze data acquired with
|bfrescoxpro|.

Requirements
^^^^^^^^^^^^
.. _Meson: https://mesonbuild.com
.. _ninja: https://ninja-build.org
.. _Issue 17: https://github.com/bandframework/Bfrescox/issues/17
.. _Issue 30: https://github.com/bandframework/Bfrescox/issues/30

Before installing |bfrescoxpro|, users must provide a Fortran compiler that
supports all requirements for building |frescox|.  At present, installations
require either the use of the

* GCC compiler suite (``gfortran``) or
* an Intel compiler suite (``ifort`` or ``ifx``).

If OpenMP parallelization is desired, ensure that the compiler supports OpenMP
compilation.  Please consult the |frescox| documentation for more information on
its build requirements.

.. todo::

    The distribution is encoded with the version of |frescox| that will be used.
    This information is effectively hidden from the users.  Therefore, they
    won't know what version of the |frescox| documentation to refer to.  See
    `Issue 30`_.

If MPI parallelization is desired, then the user must also provide an MPI
installation that is compatible with the Fortran compiler.

The package's build system uses `Meson`_ to automatically detect external
dependencies, such as the compiler and MPI installation, and to build the
binary.  Both Meson and its backend `ninja`_ are temporarily installed
automatically during package installation.

.. note::

    Testing on some systems has revealed that the |bfrescoxpro| build system can
    fail to correctly use properly installed non-Open MPI installations (|eg|
    MPICH).  This is presently under investigation (See `Issue 17`_) and a
    potential workaround is to insist that MPI be used in the build

    .. code:: console

        $ cd /path/to/Bfrescox/bfrescoxpro_pypkg
        $ BFRESCOX_USE_MPI=enabled python -m pip install .

Installation
^^^^^^^^^^^^
.. _Issue 15: https://github.com/bandframework/Bfrescox/issues/15
.. _Issue 16: https://github.com/bandframework/Bfrescox/issues/16

While we intend for this package to eventually be distributed by PyPI for direct
installation |via| |pip|, during this alpha development phase, users must
install the package directly from a local clone of the |bfrescox| repository.
By default, running

.. code:: console

    $ cd /path/to/Bfrescox/bfrescoxpro_pypkg
    $ python -m pip install .

will build a binary with OpenMP if the compiler that is found by Meson supports
OpenMP compilation.  In addition, it will build with MPI if an MPI
implementation is found by Meson.  If both are found, then an MPI+OpenMP binary
is built.  If neither is found, then please update your software stack or use
the |bfrescox| package.

Note that one can inspect the external dependencies found by the build system
and the progress of the build using ``-v`` in the above.

Users can also override customization by setting the ``BFRESCOX_USE_MPI`` and
``BFRESCOX_USE_OMP`` environment variables to

* ``disabled`` - build will not include the associated feature
* ``enabled`` - build requires the associated feature and its dependencies
* ``auto`` - include associated feature if it and its dependencies are found

For instance, to build a |frescox| binary that
must use OpenMP but that should not use MPI despite the fact that MPI is
installed, use

.. code:: console

    $ BFRESCOX_USE_MPI=disabled BFRESCOX_USE_OMP=enabled python -m pip install .

By default, ``auto`` is enabled. 

**UNOFFICIAL & UNTESTED CUSTOMIZATIONS**

If a user would like to build |frescox| using a local installation of
BLAS/LAPACK (`Issue 15`_), then they can set ``BFRESCOX_USE_LAPACK=enabled`` at
installation.

Users can also build |frescox| with extra functionality by setting

* ``BFRESCOX_USE_COREX=true`` (`Issue 16`_).

at installation.

Testing
^^^^^^^
The |bfrescoxpro| Python package has a minimal, automated test suite integrated
in the package that can be run to test an installation.  After installing the
package, the installation can be tested by executing

.. code-block:: console

    $ python
    >>> import bfrescoxpro
    >>> bfrescoxpro.__version__
    <version>
    >>> bfrescoxpro.print_information()
        ...
    >>> bfrescoxpro.test()
        ...

While users are encouraged to perform extra testing of all |bfrescox| and
|bfrescoxpro| installations, the customizability of |bfrescoxpro| installations
likely merits more extensive additional testing.

Troubleshooting
^^^^^^^^^^^^^^^
The automatic detection of the compiler and MPI implementation can be influenced
by standard build system environment variables such as ``FC`` and ``MPIFC``.

If the build system does not automatically discover the compiler, ensure that
the compiler is in the ``PATH``.  If it still fails, try

.. code:: console

    $ FC=/path/to/compiler python -m pip install .

Note that this could also be used to override the choice of compiler made by the
build system.

If the build system does not automatically discover the desired MPI
installation, ensure that at least one of the installation's ``mpif90``,
``mpifort``, ``mpiifort``, |etc| compiler wrappers is in the ``PATH``.  If it
still fails, try

.. code:: console

    $ MPIFC=/path/to/wrapper python -m pip install .

Programmatic interface
^^^^^^^^^^^^^^^^^^^^^^
While the documentation in :numref:`api_start` is geared toward |bfrescox|, it
is generally useful for |bfrescoxpro| as well.  The only differences is that in
|bfrescoxpro| the :py:func:`bfrescox.run_simulation` function has the additional
required ``mpi_setup`` argument.

The following example demonstrates the use of ``mpi_setup`` by running an
MPI+OpenMP |frescox| simulation using the given standard Fortran NML
configuration file with 5 OpenMP threads for each of 2 MPI processes.

.. code:: python

    import os

    from pathlib import Path

    import bfrescoxpro

    os.environ["OMP_NUM_THREADS"] = 5

    result = bfrescoxpro.run_simulation(
        configuration=bfrescoxpro.Configuration.from_NML("simulation.in"),
        filename=Path.cwd().joinpath("test.out"),
        mpi_setup={bfrescoxpro.N_MPI_PROCESSES: 2}
    )

Custom |frescox| binary
-----------------------

.. todo::

    * Write this once we have basic functionality in the package.
