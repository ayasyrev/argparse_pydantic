import argparse

from pydantic import BaseModel, Field

from argparse_pydantic.core import (
    add_args_from_model,
    create_model_obj,
    argument_kwargs,
)
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
    arg_int: int = Field(
        default=0,
        json_schema_extra=argument_kwargs(flag="-i"),
    )


def test_add_args_simple():
    """test basic args"""
    # base parser
    parser_base = argparse.ArgumentParser()
    parser_base.add_argument("-s", "--arg_str", type=str, default="")
    parser_base.add_argument("-i", "--arg_int", type=int, default=0)

    # parser from cfg
    parser = argparse.ArgumentParser()

    # add arguments - SimpleArg
    parser = add_args_from_model(parser, SimpleArg)
    assert parsers_args_equal(parser_base, parser)
    assert not parsers_actions_diff(parser_base, parser)
    assert parsers_actions_equal(parser_base, parser)
    assert parser_base.format_help() == parser.format_help()

    # create instance
    args = parser.parse_args(["--arg_str", "test string"])
    assert args.arg_str == "test string"
    cfg = create_model_obj(SimpleArg, args)
    assert cfg.arg_str == "test string"
    base_model_obj = SimpleArg(arg_str="test string")
    assert cfg == base_model_obj
    # short flag
    args = parser.parse_args(["-s", "test string 2"])
    assert args.arg_str == "test string 2"
    cfg = create_model_obj(SimpleArg, args)
    assert cfg.arg_str == "test string 2"
    base_model_obj = SimpleArg(arg_str="test string 2")
    assert cfg == base_model_obj

    # arg_int
    args = parser.parse_args(["-i", "2"])
    assert args.arg_int == 2
    cfg = create_model_obj(SimpleArg, args)
    assert cfg.arg_int == 2
    base_model_obj = SimpleArg(arg_int=2)
    assert cfg == base_model_obj
