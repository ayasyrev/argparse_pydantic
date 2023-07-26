import argparse

from pydantic import BaseModel, Field

from argparse_pydantic.core import (
    add_args_from_model,
    argument_kwargs,
    create_model_obj,
)
from argparse_pydantic.test_tools import (
    parsers_actions_diff,
    parsers_args_equal,
    parsers_equal,
)


def test_action_base():
    """test basic action - store true / false"""

    parser_base = argparse.ArgumentParser()
    parser_base.add_argument("--arg_1", type=bool, default=True)
    parser_base.add_argument("--arg_2", action="store_true")
    parser_base.add_argument("--arg_3", action="store_false")

    class SimpleArg(BaseModel):
        arg_1: bool = True
        arg_2: bool = Field(
            default=False,
            json_schema_extra=argument_kwargs(
                action="store_true",
            ),
        )
        arg_3: bool = Field(
            default=True,
            json_schema_extra=argument_kwargs(
                action="store_false",
            ),
        )

    parser = argparse.ArgumentParser()
    add_args_from_model(parser, SimpleArg)
    assert not parsers_actions_diff(parser_base, parser)
    assert parsers_args_equal(parser_base, parser)
    assert parsers_equal(parser_base, parser)

    args = parser.parse_args([])
    cfg = create_model_obj(SimpleArg, args)
    assert cfg == SimpleArg()

    args = parser.parse_args(["--arg_2"])
    cfg = create_model_obj(SimpleArg, args)
    assert cfg == SimpleArg(arg_2=True)

    args = parser.parse_args(["--arg_3"])
    cfg = create_model_obj(SimpleArg, args)
    assert cfg == SimpleArg(arg_3=False)


def test_action_wrong():
    """test basic action - store true wrong"""

    class SimpleArgWrong1(BaseModel):
        arg_1: int = Field(
            default=True,
            json_schema_extra=argument_kwargs(
                action="store_true",
            ),
        )

    parser = argparse.ArgumentParser()
    try:
        add_args_from_model(parser, SimpleArgWrong1)
    except ValueError as err:
        assert str(err) == "action store_true doesn't match default True"

    class SimpleArgWrong2(BaseModel):
        arg_1: int = Field(
            default=False,
            json_schema_extra=argument_kwargs(
                action="store_false",
            ),
        )

    parser = argparse.ArgumentParser()
    try:
        add_args_from_model(parser, SimpleArgWrong2)
    except ValueError as err:
        assert str(err) == "action store_false doesn't match default False"
