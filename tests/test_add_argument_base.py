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


def test_add_help_def_type():
    """test add help_def_type"""
    class Cfg1(BaseModel):
        arg_int: int

    parser = create_parser()
    add_args_from_model(parser, Cfg1, help_def_type=True)

    assert "positional arguments:\n  arg_int     [int]\n" in parser.format_help()

    parser = create_parser()
    add_args_from_model(parser, Cfg1, undefined_positional=False, help_def_type=True)
    help_str = parser.format_help()
    assert "--arg_int ARG_INT  [int]\n" in help_str

    class Cfg2(BaseModel):
        arg_int: int = 0
        arg_float: float = 0.1

    parser = create_parser()
    add_args_from_model(parser, Cfg2, help_def_type=True)
    help_str = parser.format_help()
    assert "[int] default: 0\n" in help_str
    assert "[float] default: 0.1\n" in help_str
