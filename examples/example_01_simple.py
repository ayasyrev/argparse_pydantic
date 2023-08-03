# Basic example - create base config for you app with typed config based on pydantic.
import argparse

from pydantic import BaseModel

from argparse_pydantic.core import add_args_from_model, create_model_obj

# for tests
from argparse_pydantic.test_tools import parsers_equal


# Create config for App as BaseModel
class AppCfg(BaseModel):
    arg_1: int = 0
    arg_2: float = 0.1
    arg_3: str = "string"


# create argparse.ArgumentParser as usual
parser = argparse.ArgumentParser()
# add arguments to parser from our config
add_args_from_model(parser, AppCfg)

# Result parser will be same as below
parser_base = argparse.ArgumentParser()
parser_base.add_argument("--arg_1", type=int, default=0)
parser_base.add_argument("--arg_2", type=float, default=0.1)
parser_base.add_argument("--arg_3", type=str, default="string")


if __name__ == "__main__":
    # parse arguments as usual. We got Namespace without typing
    args_namespace = parser.parse_args()
    # create config object from arguments.
    cfg: AppCfg = create_model_obj(AppCfg, args_namespace)  # type: ignore
    # now we got object with autocompletion at ide.
    # if you want to play with config at jupyter notebook: import AppCfg.
    print(cfg)
    # lets compare parsers
    assert parsers_equal(parser_base, parser)
    # test compare results
    args_base = parser_base.parse_args()
    assert args_namespace == args_base
