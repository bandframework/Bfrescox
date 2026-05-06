#!/usr/bin/env python

import os
import sys
import json
import shutil
import argparse
import traceback

from pathlib import Path


def run_test_suite(test_suite, use_pro, results_path, log_info):
    """
    .. todo::
        * This should likely be a function in common that is made available by
          the public interface such as bfrescox[pro].tests.run_test_suite so
          that tools such as this can run it as well as all related unittests in
          the package.
        * Create a function that errors checks the contents of a test suite
          object?
    """
    SYSTEM_TEMPLATE_NML = "system_template.nml"
    FRESCOX_NML = "frescox.in"
    FRESCOX_LOG = "frescox.log"

    # ----- LOGGERS
    def log(msg="", end="\n", flush=False):
        if log_info:
            print(msg, end=end, flush=flush)

    def log_and_fail(my_exception, msg):
        print(f"ERROR: {msg}")
        raise my_exception(msg)

    # ----- DETERMINE WHICH PACKAGE TO USE
    if use_pro:
        pkg_name = "Bfrescoxpro"
        try:
            from bfrescoxpro import (
                generate_elastic_template, generate_inelastic_template,
                information, run_simulation,
                parse_performance_results, parse_parallelization_setup,
                Configuration
            )
        except ModuleNotFoundError:
            print(
                "Please install the bfrescoxpro package.\n"
                "To test the bfrescox package do not use --pro."
            )
            raise
    else:
        pkg_name = "Bfrescox"
        try:
            from bfrescox import (
                generate_elastic_template, generate_inelastic_template,
                run_simulation, parse_performance_results,
                Configuration
            )
        except ModuleNotFoundError:
            print("Please install the bfrescox package")
            raise

    # ----- LOG INFO & CREATE RESULTS FOLDER
    log()
    log(f"{pkg_name} Test Suite Execution")
    log("-" * 80)
    log(f"Results Path\t\t{results_path}")
    log()

    if results_path.exists():
        log_and_fail(IsADirectoryError, f"{results_path} already exists")
    os.mkdir(results_path)

    # ----- WALK ALL TESTS IN SUITE, RUN, & SANITY CHECK
    for template_name, template_set in test_suite.items():
        log(f"{template_name} Tests")
        log("-" * 65)

        template_path = results_path.joinpath(template_name)
        if template_path.exists():
            log_and_fail(IsADirectoryError, f"{template_path} already exists")
        os.mkdir(template_path)

        for system, specification in template_set.items():
            system_path = template_path.joinpath(system)
            if system_path.exists():
                log_and_fail(IsADirectoryError, f"{system_path} already exists")
            os.mkdir(system_path)

            template_fname = system_path.joinpath(SYSTEM_TEMPLATE_NML)
            log(f"{system} Test System")
            log("-" * 50)

            # Generate template file that will be used identically for all test
            # points associated with this test system.
            #
            # Since we likely need folder names to be identical for later
            # regression testing, we perform case-sensitive template name
            # checks.
            if template_name == "Elastic":
                generate_elastic_template(
                    template_fname, **specification["ProblemConfig"]
                )
            elif template_name == "Inelastic":
                generate_inelastic_template(
                    template_fname, **specification["ProblemConfig"]
                )
            elif template_name == "User":
                user_template = Path(specification["Template"]).resolve()
                if not user_template.is_file():
                    log_and_fail(
                        FileNotFoundError,
                        f"{user_template} does not exist or is not a file"
                    )
                log(f"User-provided template\t{user_template}")
                shutil.copy(user_template, template_fname)
            else:
                log_and_fail(NotImplementedError,
                             f"Invalid template name {template_name}")

            log(f"System NML Template\t{template_fname}")

            # Run all test cases associated with the current test system
            for test_name, test_info in specification["Tests"].items():
                test_path = system_path.joinpath(test_name)
                if test_path.exists():
                    log_and_fail(IsADirectoryError,
                                 f"\n{test_path} already exists")
                os.mkdir(test_path)

                nml_fname = test_path.joinpath(FRESCOX_NML)
                std_fname = test_path.joinpath(FRESCOX_LOG)

                template_parameters = test_info["TemplateParameters"]

                cfg = Configuration.from_template(
                    template_fname,
                    nml_fname,
                    template_parameters,
                    overwrite=False,
                )
                # TODO: If we are passing in test_path, then why do we pass
                # std_fname as a filename with a full path, which could write
                # those results to a folder different from test_path?  If this
                # is the case, can't we just log to a hardcoded filename?
                #
                # The folder should effectively be the Frescox "output file" and
                # always contain all outputs generated by Frescox.
                assert not std_fname.exists()
                if use_pro:
                    mpi_setup = None
                    pro_setup = test_info["ProSetup"]

                    info = information()
                    if info["supports_mpi"]:
                        n_mpi_procs = pro_setup["nMpiProcs"]
                        mpi_setup = {"n_processes": n_mpi_procs}
                    if info["supports_openmp"]:
                        n_threads = pro_setup["nOmpThreads"]
                        os.environ["OMP_NUM_THREADS"] = str(n_threads)

                    msg = (
                        f"{test_name} Test Point / "
                        f"{n_mpi_procs} MPI Procs / "
                        f"{n_threads} Threads/Proc ... "
                    )
                    log(msg, end="", flush=True)
                    run_simulation(cfg,
                                   std_fname,
                                   mpi_setup=mpi_setup,
                                   cwd=test_path)
                    parallel_setup = parse_parallelization_setup(std_fname)
                    assert parallel_setup == (n_mpi_procs, n_threads)

                    perf_df = parse_performance_results(std_fname)
                    assert len(perf_df) == n_mpi_procs
                    max_wtime_sec = perf_df.walltime_sec.max()
                    log(f"Max Walltime={max_wtime_sec} seconds", flush=True)
                else:
                    log(f"{test_name} Test Point ... ", end="", flush=True)
                    run_simulation(cfg, std_fname, cwd=test_path)

                    perf_df = parse_performance_results(std_fname)
                    assert len(perf_df) == 1
                    log(f"Walltime={perf_df.walltime_sec[0]} seconds",
                        flush=True)

        log()


def main():
    # ----- HARDCODED VALUES
    # CI-compatible exit codes
    SUCCESS = 0
    FAILURE = 1
    # ----- SPECIFY COMMAND LINE USAGE
    DESCRIPTION = "Run the given test suite with internal sanity checks"
    TEST_SUITE_HELP = "Path to JSON-format Bfrescox test suite specification"
    OUTPUT_HELP = "Path of folder to which all results should be written"
    PRO_HELP = "Use the Bfrescoxpro package"
    QUIET_HELP = "Disable all optional logging"
    DEBUG_HELP = "Print information to help debug this script"
    parser = argparse.ArgumentParser(
        description=DESCRIPTION, formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("suite", nargs=1, type=str, help=TEST_SUITE_HELP)
    parser.add_argument("results", nargs=1, type=str, help=OUTPUT_HELP)
    parser.add_argument("--pro", action='store_true', help=PRO_HELP)
    parser.add_argument("--quiet", "-q", action='store_true', help=QUIET_HELP)
    parser.add_argument("--debug", "-d", action='store_true', help=DEBUG_HELP)

    # ----- GET COMMAND LINE ARGUMENTS
    args = parser.parse_args()
    filename = Path(args.suite[0]).resolve()
    results_path = Path(args.results[0]).resolve()
    use_pro = args.pro
    be_quiet = args.quiet

    def log_and_abort(msg):
        print()
        print(f"ERROR: {msg}")
        print()
        if args.debug:
            traceback.format_exc()
        sys.exit(FAILURE)

    # ----- LOAD TEST SUITE
    if not filename.is_file():
        log_and_abort(f"{filename} does not exist or is not a file")
    with open(filename, "r") as fptr:
        test_suite = json.load(fptr)

    # ----- ACQUIRE TEST RESULTS
    try:
        run_test_suite(test_suite, use_pro, results_path, not be_quiet)
    except Exception:
        log_and_abort("Unable to run test suite successfully")

    return SUCCESS


if __name__ == "__main__":
    sys.exit(main())
