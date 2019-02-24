# -*- coding:utf-8 -*-


"""
Small script that runs all unit tests and checks their coverage for the
humanrenderer module. If all tests pass, and coverage PERCENTAGE is above
the number given as parameter, the script exits with 0, otherwise 1.
"""

import sys
import coverage
import argparse
#
import environment  # noqa: F401
import utest


if __name__ == "__main__":
    #
    print("\n\n")
    print("==================================================================")
    print("               STARTED UTEST WITH COVERAGE")
    print("==================================================================")
    #
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--min_coverage_percent",
                        type=float, default=100.0,  # perfect cov. default
                        help="A float between 0.0 and 100.0 expressing the \
                        minimal code coverage required to succeed")
    args = parser.parse_args()
    #
    COV_PERCENT = args.min_coverage_percent
    assert 0.0 <= COV_PERCENT <= 100.0,\
        "argument -p has to be between 0 and 100 and was " + str(COV_PERCENT)

    # wrap the testing with the coverage analyzer:
    c = coverage.Coverage(data_file="dummy_value", data_suffix=True,
                          branch=True, source=["humanrenderer"])

    # perform unit tests, wraped with the coverage instance
    c.start()
    test_results = utest.run_all_tests()
    c.stop()

    # at this point c.save() and c.xml_report(outfile=etc) would generate
    # persistent analysis files (html for interactive inspection).
    # This instead handles the data within Python:
    cov_percentage = c.report()
    #
    num_tests = test_results.testsRun
    num_errors = len(test_results.errors)
    num_failures = len(test_results.failures)
    #
    print("This script did", num_tests, "tests in total.")
    print("No. of test errors:", num_errors)
    print("No. of test failures:", num_failures)
    print("Code coverage of tests (percentage):", cov_percentage)
    print("Code coverage required was:", COV_PERCENT)
    print("==================================================================")
    print("\n\n")
    #
    if num_errors > 0 or num_failures > 0 or cov_percentage < COV_PERCENT:
        sys.exit(1)
    else:
        # exit(0) means all went well
        sys.exit(0)