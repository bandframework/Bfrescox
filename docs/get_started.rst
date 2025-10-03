Getting Started
===============

General Installations
---------------------
While we intend for this package to eventually be distributed by PyPI for direct
installation |via| |pip|, during this alpha development phase, users must
install the package directly from a local clone of the |bfrescox| repository.
For developer installations, refer to the :numref:`tox_usage:Developer
Environment`.

Installation from local clone
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
After setting up your target ``python`` environment as desired, execute

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
