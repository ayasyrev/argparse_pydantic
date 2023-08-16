# Basic example - create base config for you app with typed config based on pydantic.
import argparse


# Result parser will be same as below
parser = argparse.ArgumentParser()
parser.add_argument("--arg_1", type=int, default=0)
parser.add_argument("--arg_2", type=float, default=0.1)
parser.add_argument("--arg_3", type=str, default="string")


if __name__ == "__main__":
    # parse arguments as usual. We got Namespace without typing
    cfg = parser.parse_args()
    print(f"{cfg.arg_1=}")
    print(f"{cfg.arg_2=}")
    print(f"{cfg.arg_3=}")
