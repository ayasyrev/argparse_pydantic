# Example 5 - repeat python docs for argparse example.
# https://docs.python.org/3/library/argparse.html#core-functionality
# Core Functionality
import argparse
from typing import Optional

from pydantic import BaseModel, Field

from argparse_pydantic.core import add_args_from_model, argument_kwargs, create_model_obj
from argparse_pydantic.helpers import ArgumentParserCfg, create_parser
from argparse_pydantic.test_tools import parsers_actions_diff, parsers_equal_typed


# create parser
parser = argparse.ArgumentParser(
    prog="ProgramName",
    description="What the program does",
    epilog="Text at the bottom of help",
)

# We can use same parser, but we can create in from config.
parser_cfg = ArgumentParserCfg(
    prog="ProgramName",
    description="What the program does",
    epilog="Text at the bottom of help",
)
parser_2 = create_parser(parser_cfg)


# basic example from docs.
parser.add_argument("filename")  # positional argument
parser.add_argument("-c", "--count")  # option that takes a value
parser.add_argument("-v", "--verbose", action="store_true")  # on/off flag


# We create config for App
class AppCfg(BaseModel):
    filename: str = Field(json_schema_extra=argument_kwargs(positional=True))  # positional argument
    count: Optional[str] = Field(
        default=None,
        json_schema_extra=argument_kwargs(
            flag="-c",
        )
    )  # option that takes a value
    verbose: bool = Field(
        default=False,
        json_schema_extra=argument_kwargs(
            flag="-v",
            action="store_true"
        )  # on/off flag
    )


# now we add arguments from config
add_args_from_model(parser_2, AppCfg)

# compare
assert parsers_equal_typed(parser, parser_2)

# parsers equal
# difference is [{'type': (None, <class 'str'>)}, {'type': (None, <class 'str'>)}]
# if we didn't set type at argparse it will be None at parser, after parse it will be str.
# we set type for this argument as str.
diff = parsers_actions_diff(parser, parser_2)
# print(diff)


if __name__ == "__main__":
    # parse arguments.
    # parse_args return object from config Class (based on BaseModel) sent to it as argument.
    # if you want some config to parser, you can send it as argument to parse_args

    # we got positional argument here, so for testing we pass to parser some value
    args = parser_2.parse_args(["some_filename"])
    print(args)
    # args = parser.parse_args()
    cfg: AppCfg = create_model_obj(AppCfg, args)
    # now we got object with autocompletion at ide.
    # if you want to play with config at jupyter notebook: import AppCfg.
    # print(cfg)
    # assert cfg == AppCfg()
    expected = AppCfg(filename="some_filename")
    # print(expected)
    assert cfg == expected
