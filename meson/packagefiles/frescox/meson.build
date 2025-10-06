# ----- SPECIFY PROJECT
# Build minimal, bare-bones executable by default.
#
# Users should refer to Frescox documentation for information on its version
# history and licensing.
project('frescox', 'fortran',
        meson_version: '>=1.6.0',
        version: 'n/a',
        license: 'Check Frescox repository',
        license_files: 'LICENSE',
        default_options: [
          'buildtype=debug',
          'fortran_std=legacy',
          'default_library=shared',
          'b_ndebug=if-release',
          'b_pch=false',
          'unity=off',
          'use_mpi=disabled',
          'use_openmp=disabled',
          'use_lapack=disabled',
          'use_corex=false'
        ])

# ----- LOAD ALL SOURCE FILES
subdir('source')

# ----- WE NEED TO PREPROCESS ALL FILES
fc = meson.get_compiler('fortran')
if fc.get_id() == 'gcc'
    add_project_arguments('-cpp', language: 'fortran')
    if fc.get_linker_id() == 'ld64'
        # It appears that for macOS the hard limit for the stack size cannot be
        # changed much less set to unlimited.  Therefore, this is necessary to
        # avoid stack overflows.
        add_project_link_arguments('-Wl,-stack_size,0x20000000', language: 'fortran')
    endif
elif (fc.get_id() == 'intel') or (fc.get_id() == 'intel-llvm')
    add_project_arguments('-fpp', language: 'fortran')
else
    error('Unknown compiler suite')
endif

# ----- DEPENDENCIES
deps_all = []

openmp_dep = dependency('openmp', language: 'fortran',
                        required: get_option('use_openmp'))
if openmp_dep.found()
    deps_all += [openmp_dep]
endif

mpi_dep = dependency('mpi', language: 'fortran',
                     required: get_option('use_mpi'))
if mpi_dep.found()
    add_project_arguments('-DMPI', language: 'fortran')
    # This works with both OpenMPI & MPICH beginning with v1.6.0.  See
    # https://github.com/mesonbuild/meson/pull/13619
    deps_all += [mpi_dep]
    src_parallel = [src_parallel_mpi]
else
    src_parallel = [src_parallel_no_mpi]
endif

# Meson is looking into a single dependence for finding OpenBlas/Netlib/MKL for
# example.
# https://github.com/mesonbuild/meson/issues/2835
#
# For now, we just use pkg-config.  This works with Netlib-LAPACK install in
# macOS via homebrew.
blas_dep   = dependency('blas',   method: 'pkg-config',
                        required: get_option('use_lapack'))
lapack_dep = dependency('lapack', method: 'pkg-config',
                        required: get_option('use_lapack'))
if blas_dep.found() and lapack_dep.found()
    deps_all += [blas_dep, lapack_dep]
    src_blas = []
else
    src_blas = [src_lapack_stub]
endif

src_nag = [src_nag_stub]

# ----- SITE/COMPILER-SPECIFIC CODE
if fc.get_id() == 'gcc'
    if openmp_dep.found() and mpi_dep.found()
        src_local = [src_f14gfortran_mpi_omp]
    elif openmp_dep.found()
        src_local = [src_f14gfortran_omp]
    elif mpi_dep.found()
        src_local = [src_f14gfortran_mpi]
    else
        src_local = [src_f14gfortran]
    endif
elif (fc.get_id() == 'intel') or (fc.get_id() == 'intel-llvm')
    if openmp_dep.found() and mpi_dep.found()
        src_local = [src_f14intel_mpi_omp]
    elif openmp_dep.found()
        src_local = [src_f14intel_omp]
    elif mpi_dep.found()
        src_local = [src_f14intel_mpi]
    else
        src_local = [src_f14intel]
    endif
else
    error('Unknown compiler suite')
endif

# ----- USER ARGUMENTS
# Run this after dependencies so that we can alter dependencies according to
# the user's needs.
if get_option('use_corex')
    add_project_arguments('-Dcorex', language: 'fortran')
endif

# ----- WRITE SETUP TO FILE
config = configuration_data()
config.set('found_mpi',    mpi_dep.found())
config.set('found_openmp', openmp_dep.found())
config.set('found_lapack', blas_dep.found() and lapack_dep.found())
config.set('use_corex',    get_option('use_corex'))

configure_file(input:         'build_info.template',
               output:        'build_info.csv',
               configuration: config,
               install:       true,
               install_dir:   'build')

# ----- BUILD ALL FRESCOX BINARIES
exe_src = src_base + src_bins + src_search + src_parallel + src_local + src_nag + src_blas
frescox_src  = exe_src + frescox_main_src

# TODO: Precompile all Fortran files and pass those to builds.  This will let
# Meson determine what the precompiler flag is for each compiler suite.  I also
# like the idea of the dependency engine looking for dependencies after
# preprocessing.  See fc.preprocess().

executable('frescox', frescox_src,
           dependencies: deps_all,
           install: true)
