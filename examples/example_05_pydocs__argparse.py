# Example 5 - repeat python docs for argparse example.
# same as example_05_help.py but with argparse as at docs
# https://docs.python.org/3/library/argparse.html#core-functionality
# Core Functionality
import argparse


# create parser
parser = argparse.ArgumentParser(
    prog="ProgramName",
    description="What the program does",
    epilog="Text at the bottom of help",
)

parser.add_argument("filename")  # positional argument
parser.add_argument("-c", "--count")  # option that takes a value
parser.add_argument("-v", "--verbose", action="store_true")  # on/off flag


if __name__ == "__main__":
    # parse arguments.
    args = parser.parse_args()
    # args is Namespace object.
    print(f"filename={args.filename}")
    print(f"count={args.count}")
    print(f"verbose={args.verbose}")
