# The Meson build system for the Bfrescoxpro Python package.  In particular, it
# is responsible for collecting user build preferences, if any, and passing
# these to the Frescox build system, which is declared as a required subpackage
# of this build system.
#
# Version is communicated through the package's version information.

# Use conservative Frescox build flags by default
project('bfrescoxpro', 'fortran',
        meson_version: '>=1.6.0',
        license:       'BSD-2-Clause',
        license_files: 'LICENSE',
        default_options: [
          'use_mpi=disabled',
          'use_openmp=disabled',
          'use_lapack=disabled',
          'use_corex=false'
        ])

# -- Relay Bfrescoxpro build flags to Frescox build system
# Options that are features are special and need the translation.
# Booleans do not.

# Frescox optional features
use_corex = get_option('use_corex')

# MPI
feature = get_option('use_mpi')
if feature.enabled()
    use_mpi = 'enabled'
elif feature.auto()
    use_mpi = 'auto'
else
    use_mpi = 'disabled'
endif

# OpenMP
feature = get_option('use_openmp')
if feature.enabled()
    use_openmp = 'enabled'
elif feature.auto()
    use_openmp = 'auto'
else
    use_openmp = 'disabled'
endif

# BLAS/LAPACK
feature = get_option('use_lapack')
if feature.enabled()
    use_lapack = 'enabled'
elif feature.auto()
    use_lapack = 'auto'
else
    use_lapack = 'disabled'
endif

pro_options = {'use_mpi':    use_mpi,
               'use_openmp': use_openmp,
               'use_lapack': use_lapack,
               'use_corex':  use_corex}
subproject('frescox', required: true, default_options: pro_options)
