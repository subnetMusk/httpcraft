import argparse
import sys, os

# Aggiungiamo la root del progetto al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

def main():
    parser = argparse.ArgumentParser(
    description="HttpCraft - HTTP request crafting and inspection tool"
    )
    parser.add_argument("--run-tests", action="store_true", help="Run internal test suite")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output for --run-tests")

    args = parser.parse_args()

    if args.run_tests:
        from tests.runtests import run_from_cli
        run_from_cli(verbose=args.verbose)
    else:
        print("HttpCraft - HTTP client library\n")
        print("This tool is meant to be imported and used in Python code.")
        print("\nAvailable CLI option:")
        print("  --run-tests     Run internal tests and check installation")
        print("\nExample:")
        print("  import http_craft\n  client = http_craft.HttpCraft('http://example.com')")

if __name__ == "__main__":
    main()