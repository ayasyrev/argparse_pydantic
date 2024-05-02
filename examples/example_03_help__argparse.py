# Example 3 - create config with helps.
# same as example_03_help.py but with argparse
import argparse

parser = argparse.ArgumentParser(
    prog="name", description="example prog", epilog="nothing done, just example..."
)
parser.add_argument("--arg_1", type=int, default=0, help="argument 1, int")
parser.add_argument(
    "-s",
    "--arg_2",
    type=str,
    default="",
    help="string arg, can be used with short flag -s",
)
parser.add_argument("-f", "--arg_3", type=float, default=0.0)


if __name__ == "__main__":
    args = parser.parse_args()
    # args is Namespace object
    print(f"arg_1={args.arg_1}")
    print(f"arg_2={args.arg_2}")
    print(f"arg_3={args.arg_3}")
