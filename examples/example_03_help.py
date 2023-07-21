# Example 3 - create config with helps.
import argparse

from pydantic import BaseModel, Field  # only for tests

from argparse_pydantic import ArgumentParserCfg, add_args_from_model, parse_args

# for tests
from argparse_pydantic import create_parser
from argparse_pydantic.test_tools import parsers_equal


# Create config for parser
parser_cfg = ArgumentParserCfg(
    prog="name", description="example prog", epilog="nothing done, just example..."
)


# Create config for App
class AppCfg(BaseModel):
    arg_1: int = Field(
        default=0,
        # add help
        description="argument 1, int",
    )
    arg_2: str = Field(
        default="",
        # short flag can be add as json_schema_extra
        json_schema_extra={"flag": "s"},
        description="string arg, can be used with short flag -s",
    )


# result parser will be same as below
parser_base = argparse.ArgumentParser(
    prog="name", description="example prog", epilog="nothing done, just example..."
)
parser_base.add_argument("--arg_1", type=int, default=0, help="argument 1, int")
parser_base.add_argument(
    "-s",
    "--arg_2",
    type=str,
    default="",
    help="string arg, can be used with short flag -s",
)


if __name__ == "__main__":
    # parse arguments.
    # parse_args return object from config class (BaseModel) sent to it as argument.
    cfg: AppCfg = parse_args(AppCfg, parser_cfg=parser_cfg)
    # now we got object with autocompletion at ide.
    # if you want to play with config at jupyter notebook: import AppCfg.
    print(cfg)

    # Tests
    args_base = parser_base.parse_args()
    parser = create_parser(parser_cfg)
    add_args_from_model(parser, AppCfg)
    assert parsers_equal(parser, parser_base)
    args = parser.parse_args()
    assert args == args_base
