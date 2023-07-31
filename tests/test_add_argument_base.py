import argparse

from pydantic import BaseModel, Field

from argparse_pydantic.core import add_args_from_model
from argparse_pydantic.helpers import create_parser
from argparse_pydantic.test_tools import parsers_args_equal, parsers_equal


def test_add_args_base():
    """test basic args positional / optional"""
    # base parser, positional
    parser_base = argparse.ArgumentParser()
    parser_base.add_argument("arg_int", type=int)

    class Cfg1(BaseModel):
        arg_int: int

    parser = create_parser()
    add_args_from_model(parser, Cfg1)

    assert parsers_args_equal(parser_base, parser)

    # base parser, optional
    parser_base = argparse.ArgumentParser()
    parser_base.add_argument("--arg_int", type=int, required=True)

    parser = create_parser()
    add_args_from_model(parser, Cfg1, undefined_positional=False)

    assert parsers_args_equal(parser_base, parser)

    # base parser, positional through json_schema_extra
    parser_base = argparse.ArgumentParser()
    parser_base.add_argument("arg_int", type=int)
    parser_base.add_argument("--arg_float", type=float, required=True)

    class Cfg2(BaseModel):
        arg_int: int = Field(json_schema_extra={"positional": True})
        arg_float: float

    parser = create_parser()
    add_args_from_model(parser, Cfg2, undefined_positional=False)

    assert parsers_equal(parser_base, parser)
