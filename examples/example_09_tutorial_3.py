# Example 9 - repeat examples from python tutorial for argparse.
# https://docs.python.org/3/howto/argparse.html#introducing-optional-arguments
# Introducing Optional arguments
import argparse

from pydantic import BaseModel, Field

from argparse_pydantic import add_args_from_model, create_model_obj
from argparse_pydantic.core import argument_kwargs

from argparse_pydantic.test_tools import parsers_equal, parsers_equal_typed


# create parser
parser = argparse.ArgumentParser()
parser.add_argument("--verbosity", help="increase output verbosity")


# create config for App
class AppCfg(BaseModel):  # type: ignore
    # as by default argparse parsed arguments from command line as str
    verbosity: str = Field(description="increase output verbosity")


# create parser and add arguments from config class.
parser_2 = argparse.ArgumentParser()
add_args_from_model(parser_2, AppCfg)

# parsers are equal
assert parsers_equal_typed(parser, parser_2)

# lets parse arguments
cl_arg = ["--verbosity", "1"]
# we got Namespace object from parser
args = parser.parse_args(cl_arg)
args_2 = parser_2.parse_args(cl_arg)
assert args.verbosity == args_2.verbosity == "1"
# # but we can convert Namespace to config object with types and autocomplete at ide
cfg: AppCfg = create_model_obj(AppCfg, args)
assert cfg.verbosity == args.verbosity == "1"


# as at tutorial lets modify parser
parser = argparse.ArgumentParser()
parser.add_argument("--verbose", help="increase output verbosity", action="store_true")


class AppCfg(BaseModel):  # pylint: disable=function-redefined
    verbose: bool = Field(
        default=False,
        json_schema_extra=argument_kwargs(
            help="increase output verbosity",
            action="store_true",
        )
    )


parser_2 = argparse.ArgumentParser()
add_args_from_model(parser_2, AppCfg)

assert parsers_equal(parser, parser_2)

cl_arg = ["--verbose"]

args = parser.parse_args(cl_arg)
args_2 = parser_2.parse_args(cl_arg)
assert args.verbose == args_2.verbose
assert args.verbose is True
# # but we can convert Namespace to BaseModel object with types and autocomplete at ide
cfg: AppCfg = create_model_obj(AppCfg, args)
assert cfg.verbose == args.verbose
assert cfg.verbose is True
