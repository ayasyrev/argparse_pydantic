# Example 8 - repeat examples from python tutorial for argparse.
# https://docs.python.org/3/howto/argparse.html#introducing-positional-arguments
# Introducing Positional arguments
import argparse

from pydantic import BaseModel, Field

from argparse_pydantic import add_args_from_model, create_model_obj
from argparse_pydantic.core import argument_kwargs
from argparse_pydantic.test_tools import parsers_equal_typed

# create parser
parser = argparse.ArgumentParser()
parser.add_argument("square", help="display a square of a given number", type=int)


# create config for App
class AppCfg(BaseModel):
    square: int = Field(
        json_schema_extra=argument_kwargs(
            help="display a square of a given number",
        )
    )


# create parser and add arguments from config
parser_2 = argparse.ArgumentParser()
add_args_from_model(parser_2, AppCfg)

# parsers are equal
assert parsers_equal_typed(parser, parser_2)


# lets parse arguments
cl_arg = ["4"]
# we got Namespace object from parser
args = parser.parse_args(cl_arg)
args_2 = parser_2.parse_args(cl_arg)
assert args.square == args_2.square

# but we can convert Namespace to model object with types and autocomplete at ide
cfg: AppCfg = create_model_obj(AppCfg, args)
assert cfg.square == args.square
