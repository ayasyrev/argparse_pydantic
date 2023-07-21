import argparse

from pydantic import BaseModel, Field

from argparse_pydantic.core import add_args_from_model, create_model_obj
from argparse_pydantic.test_tools import (
    parsers_actions_diff,
    parsers_actions_equal,
    parsers_args_equal,
)


class SimpleArg(BaseModel):
    arg_str: str = Field(
        default="",
        json_schema_extra={"flag": "s"},
    )


def test_add_args_simple():
    """test basic args"""
    # base parser
    parser_base = argparse.ArgumentParser()
    # parser_base.add_argument("--arg_int", type=int, required=True)
    # parser_base.add_argument("--arg_int", type=int)
    # parser_base.add_argument("--arg_float", type=float, default=0.0)
    parser_base.add_argument("-s", "--arg_str", type=str, default="")

    # parser from cfg
    parser = argparse.ArgumentParser()

    # add arguments - SimpleArg
    parser = add_args_from_model(parser, SimpleArg)
    assert parsers_args_equal(parser_base, parser)
    assert not parsers_actions_diff(parser_base, parser)
    assert parsers_actions_equal(parser_base, parser)
    assert parser_base.format_help() == parser.format_help()

    # create instance
    # args = parser.parse_args(["--arg_int", "1"])
    args = parser.parse_args(["--arg_str", "test string"])
    assert args.arg_str == "test string"
    cfg = create_model_obj(SimpleArg, args)
    assert cfg.arg_str == "test string"
    base_model_obj = SimpleArg(arg_str="test string")
    assert cfg == base_model_obj
