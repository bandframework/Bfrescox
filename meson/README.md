Each Bfrescox Python package contains its own Meson-based build system, which is
invoked by its `setup.py` during installation.  This build system lists a
specific version of Frescox as an external, required subpackage so that the
correct version of Frescox is built automatically during the Python package
installation.  To accomplish such nested build systems, Bfrescox must provide a
Meson-based build system for Frescox.  This is also necessary because the Meson
build system provided here is capable of automatic external dependence discovery
(e.g., MPI, BLAS), which is required to satisfy Bfrescox distribution
requirements.

This folder contains
* a Meson build system wrapper (``frescox.wrapper``) that is used by the build
  system of each Bfrescox Python package to clone and use the appropriate
  version of Frescox for building its internal Frescox binary
* a Meson build system (``packagefiles``) for use with the local Frescox clone
  for building the internal Frescox binary with automatic external dependence
  discovery

Note that the current implementation of the package build systems are such that
both packages build their internal Frescox binaries from the same commit, which
is sensible.
