import argparse

from pydantic import BaseModel

from argparse_pydantic.core import add_args_from_model, create_model_obj
from argparse_pydantic.test_tools import (
    parsers_actions_diff,
    parsers_actions_equal,
    parsers_args_equal,
)


class SimpleArg(BaseModel):
    arg_int: int
    arg_float: float = 0.0
    arg_str: str = ""


def test_add_args_simple():
    """test basic args"""
    # base parser
    parser_base = argparse.ArgumentParser()
    parser_base.add_argument("--arg_int", type=int, required=True)
    parser_base.add_argument("--arg_float", type=float, default=0.0)
    parser_base.add_argument("--arg_str", type=str, default="")

    # parser from cfg
    parser = argparse.ArgumentParser()

    # add arguments - SimpleArg
    parser = add_args_from_model(parser, SimpleArg)
    assert parsers_args_equal(parser_base, parser)
    assert not parsers_actions_diff(parser_base, parser)
    assert parsers_actions_equal(parser_base, parser)
    assert parser_base.format_help() == parser.format_help()

    # create instance
    args = parser.parse_args(["--arg_int", "1"])
    assert args.arg_int == 1
    cfg = create_model_obj(SimpleArg, args)
    assert cfg.arg_int == 1
    base_model_obj = SimpleArg(arg_int=1)
    assert cfg == base_model_obj
