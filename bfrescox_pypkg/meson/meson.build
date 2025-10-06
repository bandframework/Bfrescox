# The Meson build system for the Bfrescox Python package.  In particular, its
# only action is to specify that Frescox is a required subpackage of this build
# system and to configure the subpackage to build only a bare-bones version of
# Frescox.
#
# The goal is for all external dependencies of the bare-bones executables to be
# only compiler and OS libraries so that this package could potentially be
# distributed as prebuilt binary wheels if this is possible and a correct,
# acceptable solution.
#
# TODO: Among other tasks, we would have to determine within the context of the
# Frescox license if distributing PyPI prebuilt binary wheels that contain
# Frescox binaries would be considered as distributing Frescox.  If so, then we
# would have to determine if the conditions of that license can be met.
#
# Version is communicated through the package's version information.

project('bfrescox',    'fortran',
        meson_version: '>=1.6.0',
        license:       'BSD-2-Clause',
        license_files: 'LICENSE')

no_extras = {'use_mpi':    'disabled',
             'use_openmp': 'disabled',
             'use_lapack': 'disabled',
             'use_corex':  false}
subproject('frescox', required: true, default_options: no_extras)
