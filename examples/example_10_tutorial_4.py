# Example 10 - repeat examples from python tutorial for argparse.
# https://docs.python.org/3/howto/argparse.html#short-options
# Short options
import argparse

from pydantic import BaseModel, Field

from argparse_pydantic import add_args_from_model, create_model_obj, argument_kwargs
from argparse_pydantic.test_tools import parsers_equal


# create parser
parser = argparse.ArgumentParser()
parser.add_argument(
    "-v", "--verbose", help="increase output verbosity", action="store_true"
)


# create config for App
class AppCfg(BaseModel):  # pylint: disable=function-redefined
    verbose: bool = Field(
        default=False,
        json_schema_extra=argument_kwargs(
            flag="-v",
            help="increase output verbosity",
            action="store_true",
        )
    )


# create parser and add arguments from config
parser_2 = argparse.ArgumentParser()
add_args_from_model(parser_2, AppCfg)

# parsers are equal
assert parsers_equal(parser, parser_2)

# arguments to be parsed
cl_arg = ["--verbose"]

args = parser.parse_args(cl_arg)
args_2 = parser_2.parse_args(cl_arg)
assert args.verbose == args_2.verbose
assert args.verbose is True
# # but we can convert Namespace to config object with types and autocomplete at ide
cfg: AppCfg = create_model_obj(AppCfg, args)
assert cfg.verbose == args.verbose
assert cfg.verbose is True

# with short flag
cl_arg = ["-v"]

args = parser.parse_args(cl_arg)
args_2 = parser_2.parse_args(cl_arg)
assert args.verbose == args_2.verbose
assert args.verbose is True
# # but we can convert Namespace to config object with types and autocomplete at ide
cfg: AppCfg = create_model_obj(AppCfg, args)
assert cfg.verbose == args.verbose
assert cfg.verbose is True
