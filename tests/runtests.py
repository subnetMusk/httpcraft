import unittest
import os
import sys


# Detect verbosity from CLI or env
VERBOSE = "--verbose" in sys.argv or os.getenv("HTTPCRAFT_VERBOSE", "false").lower() == "true"
if "--verbose" in sys.argv:
    sys.argv.remove("--verbose")

# Choose verbosity level (0 = quiet, 2 = detailed)
verbosity = 2 if VERBOSE else 0

# Load tests from the 'tests' directory
suite = unittest.defaultTestLoader.discover("tests")

# Run tests with configured verbosity
runner = unittest.TextTestRunner(verbosity=verbosity)
result = runner.run(suite)

# Final standard output for CI-friendly success message
if not VERBOSE and result.wasSuccessful():
    print("Running tests with verbose=False... All tests passed successfully.")
elif not result.wasSuccessful():
    print("Some tests failed.")

def run_from_cli(verbose=False):
    here = os.path.dirname(__file__)
    suite = unittest.defaultTestLoader.discover(start_dir=here, pattern="test_*.py")
    result = unittest.TextTestRunner(verbosity=1).run(suite)

    if result.wasSuccessful():
        print("All tests passed.")
    else:
        print("Some tests failed.")