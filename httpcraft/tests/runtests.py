import unittest
import os
import sys
import subprocess
import time
import signal

# Detect verbosity from CLI or environment
VERBOSE = "--verbose" in sys.argv or os.getenv("HTTPCRAFT_VERBOSE", "false").lower() == "true"
if "--verbose" in sys.argv:
    sys.argv.remove("--verbose")

def _start_mock_server():
    tests_dir = os.path.dirname(os.path.abspath(__file__))
    mock_path = os.path.join(tests_dir, "mock_server.py")

    process = subprocess.Popen(
        [sys.executable, mock_path],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    time.sleep(1.0)
    return process

def _run_tests(verbose: bool):
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    os.chdir(root_dir)

    suite = unittest.defaultTestLoader.discover(start_dir="tests", pattern="test_*.py")
    runner = unittest.TextTestRunner(verbosity=2 if verbose else 0)
    result = runner.run(suite)
    return result

def run_from_cli(verbose=False):
    server = _start_mock_server()
    try:
        result = _run_tests(verbose)
    finally:
        server.send_signal(signal.SIGINT)
        server.wait()

    if result.wasSuccessful():
        if verbose:
            print("All tests passed.")
        else:
            print("Running tests with verbose=False... All tests passed successfully.")
    else:
        print("Some tests failed.")

if __name__ == "__main__":
    run_from_cli(verbose=VERBOSE)