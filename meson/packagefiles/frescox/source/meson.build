frescox_main_src    = files('fresco.f')
sfrescox_main_src   = files('sfresco.f')
fr2nl_main_src      = files('fr2nl.f')

src_search          = files('minuit-cern.f')
src_bins            = files('frxx4.f', 'frxx7a.f', 'frxx0.f')
src_lapack_stub     = files('lapack.f')
src_nag_stub        = files('nagstub.f')

# One and only one of these two files should be included in a build.
#
# A build should use this file if there is no MPI parallelization being used.
# It should even be used if there is OpenMP parallelization enabled.
src_parallel_no_mpi = files('frxx15.f')
# A build should use this file if there is MPI parallelization being used.  This
# includes MPI+OpenMP parallelization.
src_parallel_mpi    = files('frxx45.f')

# General sources - taken from the OBJS list in makefile
src_base = files('globx7.f',
                 'version_number.f',
                 'frxx1.f',
                 'frxx2.f',
                 'frxx3.f',
                 'frxx3b.f',
                 'frxx5.f',
                 'frxx6.f',
                 'erwinrc4.f',
                 'frxx7b.f',
                 'frxx8.f',
                 'frxx9.f',
                 'frxx10.f',
                 'frxx11.f',
                 'bincc.f',
                 'frxx13.f',
                 'frxx16.f',
                 'frxx17.f',
                 'frxx21.f',
                 'lagmesh.f',
                 'frxx27.f',
                 'frxx22.f',
                 'erwinmpi6.f',
                 'cdc.f')

# Build-specific routines
#
# Since meson is locating the MPI implementation and identifies the name of the
# MPI wrapper to use, we don't need to use all the different MPI-based variants
# in Frescox.
src_f14gfortran         = files('f14gfortran.f')
src_f14gfortran_omp     = files('f14gfortran-openmp.f')
src_f14gfortran_mpi     = files('f14gfortran-mpif90.f')
src_f14gfortran_mpi_omp = files('f14gfortran-op+mpifort.f')

src_f14intel         = files('f14intel.f')
src_f14intel_omp     = files('f14intel-openmp.f')
src_f14intel_mpi     = files('f14intel-mpich.f')
src_f14intel_mpi_omp = files('f14intel-op+mpi.f')
