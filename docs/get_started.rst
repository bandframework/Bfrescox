Getting Started
===============

The |bfrescox| package is capable of building, installing, and using a |frescox|
executable on macOS- and Linux-based systems.  Our test suite presently checks
builds with both macOS and Ubuntu.  We expect that it would work with other
similar Linux operating systems.

General Installations
---------------------

..
   - TODO : Once we merge the alpha branch into main, change the checkout command
    to "git checkout main".
   - TODO : once we have a PyPI distribution, add instructions for pip install from PyPI.

While we intend for this package to eventually be distributed by PyPI for direct
installation |via| |pip|, during this alpha development phase, users must
install the package directly from a local clone of the |bfrescox| repository. This requires checking out the ``v0.0.1-alpha`` tag after cloning the repository:

 .. code-block:: console

  $ cd /path/to/Bfrescox/
  $ git checkout v0.0.1-alpha


For developer installations, refer to the :numref:`tox_usage:Developer
Environment`.

Dependencies
^^^^^^^^^^^^
.. _Meson: https://mesonbuild.com
.. _ninja: https://ninja-build.org

Building |frescox| requires the installation of a known compiler suite including
a Fortran compiler.  At present, installations require either the use of the

* GCC compiler suite (``gfortran``) or
* an Intel compiler suite (``ifort`` or ``ifx``).

The package's build system uses `Meson`_ and its backend `ninja`_ to
automatically detect external dependencies, such as the compiler, and to build
the binary.  However, both of these dependencies are automatically installed
temporarily on behalf of users during package installation.

Installation from local clone
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. _`Bfrescox clone`: https://github.com/bandframework/Bfrescox

After installing a local `Bfrescox clone`_, you must check out the alpha branch. 

   .. code-block:: console

    $ cd /path/to/Bfrescox/
    $ git checkout v0.0.1-alpha

After setting up your target Python environment as desired, execute

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
