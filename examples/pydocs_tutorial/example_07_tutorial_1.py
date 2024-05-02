# Example 7 - repeat examples from python tutorial for argparse.
# https://docs.python.org/3/howto/argparse.html#introducing-positional-arguments
# Introducing Positional arguments
import argparse

from pydantic import BaseModel

from argparse_pydantic import add_args_from_model, create_model_obj
from argparse_pydantic.test_tools import parsers_equal_typed

# create parser
parser = argparse.ArgumentParser()
parser.add_argument("echo")


# create config for App
class AppCfg(BaseModel):
    # echo: str
    echo: str


# create parser and add arguments from config
parser_2 = argparse.ArgumentParser()
add_args_from_model(parser_2, AppCfg)

# parsers are equal
assert parsers_equal_typed(parser, parser_2)


# lets parse arguments
cl_arg = ["argument from command line"]
# we got Namespace object from parser
args = parser.parse_args(cl_arg)
args_2 = parser_2.parse_args(cl_arg)
assert args.echo == args_2.echo

# but we can convert Namespace to model object with types and autocomplete at ide
cfg: AppCfg = create_model_obj(AppCfg, args)
assert cfg.echo == args.echo
