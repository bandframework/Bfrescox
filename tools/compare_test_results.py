#!/usr/bin/env python

import sys
import json
import f90nml
import argparse
import traceback

from pathlib import Path
from compare_dataframes import compare_dataframes


def compare_test_results(test_suite, reference_path, new_path, log_info):
    """
    .. todo::
        * This should likely be a function in common that is made available by
          the public interface such as bfrescox[pro].tests.compare_test_results
          so that tools such as this can run it as well as all related unittests
          in the package.

    :return: True if all tests pass.  False, if an error occurred or any test
        failed.
    """
    # TODO: These should probably be in bfrescox[pro].tests name space so that
    # both the test execution and result comparison routines use the same
    # strings.  Note that a developer would have issues if they acquired
    # baselines with one version of the package and compared to new results
    # acquired with a different version if these keys change.  These names would
    # effectively be part of the version of our effective files.
    SYSTEM_TEMPLATE_NML = "system_template.nml"
    FRESCOX_NML = "frescox.in"

    # ----- DETERMINE WHICH PACKAGE TO USE
    # Prefer using standard bfrescox if both packages are installed
    try:
        from bfrescox import parse_fort16
        try_pro = False
    except ModuleNotFoundError:
        try_pro = True

    if try_pro:
        try:
            from bfrescoxpro import parse_fort16
        except ModuleNotFoundError:
            print("Please install the bfrescox package.")
            return False

    # ----- LOGGERS
    def log(msg=""):
        if log_info:
            print(msg)

    def log_error(msg):
        print()
        print(f"ERROR: {msg}")
        print()

    # ----- ERROR CHECK ARGUMENTS
    reference_path = Path(reference_path).resolve()
    new_path = Path(new_path).resolve()
    if not reference_path.is_dir():
        log_error(f"{reference_path} does not exist or is not a directory")
        return False
    if not new_path.is_dir():
        log_error(f"{new_path} does not exist or is not a directory")
        return False

    # ----- LOG INFO
    log()
    log("Bfrescox Regression Testing")
    log("-" * 80)
    log(f"Baselines Path\t\t{reference_path}")
    log(f"New Results Path\t{new_path}")
    log()

    # ----- WALK ALL TESTS IN SUITE & COMPARE
    # Note that we allow for the ref and new folders to have different numbers
    # of results and more results than those in the test suite.  We require only
    # that both contain results for each test case in the suite.
    for template_name, template_set in test_suite.items():
        log(f"{template_name} Tests")
        log("-" * 65)

        ref_template_path = reference_path.joinpath(template_name)
        new_template_path = new_path.joinpath(template_name)

        for system, specification in template_set.items():
            log(f"{system} Test System")
            log("-" * 50)

            ref_system_path = ref_template_path.joinpath(system)
            new_system_path = new_template_path.joinpath(system)

            # Confirm identical system-specification templates.  This assumes
            # that no insignificant changes (e.g., formating or different
            # trailing zeros) were made to the base templates between when the
            # baseline and new results were acquired.
            ref_template_fname = ref_system_path.joinpath(SYSTEM_TEMPLATE_NML)
            new_template_fname = new_system_path.joinpath(SYSTEM_TEMPLATE_NML)
            if not ref_template_fname.is_file():
                log_error(
                    f"{ref_template_fname} does not exist or is not a file"
                )
                return False
            if not new_template_fname.is_file():
                log_error(
                    f"{new_template_fname} does not exist or is not a file"
                )
                return False
            with open(ref_template_fname, "r") as fptr:
                ref_content = fptr.read()
            with open(new_template_fname, "r") as fptr:
                new_content = fptr.read()
            if ref_content != new_content:
                msg = "{} and {} have different content"
                log_error(msg.format(ref_template_fname, new_template_fname))
                return False

            for test_name, test_info in specification["Tests"].items():
                log(f"{test_name} Test Point")

                ref_test_path = ref_system_path.joinpath(test_name)
                ref_nml_fname = ref_test_path.joinpath(FRESCOX_NML)
                new_test_path = new_system_path.joinpath(test_name)
                new_nml_fname = new_test_path.joinpath(FRESCOX_NML)
                if not ref_nml_fname.is_file():
                    log_error(
                        f"{ref_nml_fname} does not exist or is not a file"
                    )
                    return False
                if not new_nml_fname.is_file():
                    log_error(
                        f"{new_nml_fname} does not exist or is not a file"
                    )
                    return False
                with open(ref_nml_fname, "r") as fptr:
                    ref_nml = f90nml.read(fptr)
                with open(new_nml_fname, "r") as fptr:
                    new_nml = f90nml.read(fptr)
                if ref_nml != new_nml:
                    msg = "{} and {} have different content"
                    log_error(msg.format(ref_nml_fname, new_nml_fname))
                    return False

                # Check all results against official baselines
                for file_type, comparison_info in test_info["Results"].items():
                    rel_diff_tolr = 0.0
                    abs_diff_tolr = 0.0

                    log(f"\tComparison Source\t\t{file_type}")
                    if "AbsDiffThreshold" in comparison_info:
                        abs_diff_tolr = comparison_info["AbsDiffThreshold"]
                        log(f"\tAbsolute Difference Threshold\t{abs_diff_tolr}")
                    if "RelDiffThreshold" in comparison_info:
                        rel_diff_tolr = comparison_info["RelDiffThreshold"]
                        log(f"\tRelative Difference Threshold\t{rel_diff_tolr}")

                    if file_type.lower() == "fort.16":
                        expected = parse_fort16(
                            ref_test_path.joinpath("fort.16")
                        )
                        results = parse_fort16(
                            new_test_path.joinpath("fort.16")
                        )
                    else:
                        log_error(f"Unknown results file type {file_type}")
                        return False

                    if set(expected) != set(results):
                        log_error(
                            "New results and baselines have different structure"
                        )
                        return False
                    for key in expected.keys():
                        try:
                            compare_dataframes(
                                results[key],
                                expected[key],
                                abs_diff_tolr,
                                rel_diff_tolr,
                            )
                        except AssertionError:
                            log_error("New results significantly different")
                            return False

            log()

    return True


def main():
    # ----- HARDCODED VALUES
    # CI-compatible exit codes
    SUCCESS = 0
    FAILURE = 1

    # ----- SPECIFY COMMAND LINE USAGE
    DESCRIPTION = "Compare new Bfrescox results against baselines"
    SUITE_HELP = "Path to JSON-format Bfrescox test suite specification"
    REFERENCE_HELP = "Path to folder containing baselines"
    NEW_HELP = "Path to folder containing new results to compare"
    QUIET_HELP = "Disable all optional logging"
    DEBUG_HELP = "Print information to help debug this script"
    parser = argparse.ArgumentParser(
        description=DESCRIPTION, formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("suite", nargs=1, type=str, help=SUITE_HELP)
    parser.add_argument("reference", nargs=1, type=str, help=REFERENCE_HELP)
    parser.add_argument("new", nargs=1, type=str, help=NEW_HELP)
    parser.add_argument("--quiet", "-q", action='store_true', help=QUIET_HELP)
    parser.add_argument("--debug", "-d", action='store_true', help=DEBUG_HELP)

    # ----- GET COMMAND LINE ARGUMENTS
    args = parser.parse_args()
    filename = Path(args.suite[0]).resolve()
    reference_path = Path(args.reference[0]).resolve()
    new_path = Path(args.new[0]).resolve()
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

    # ----- COMPARE RESULTS
    status = compare_test_results(
        test_suite, reference_path, new_path, not be_quiet
    )

    if not be_quiet:
        print()
        if status:
            print("SUCCESS")
        else:
            print("FAILURE")
        print()

    return SUCCESS if status else FAILURE


if __name__ == "__main__":
    sys.exit(main())
