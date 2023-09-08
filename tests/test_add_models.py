import argparse

from pydantic import BaseModel
from pytest import CaptureFixture

from argparse_pydantic import add_args_from_model, create_model_obj
from argparse_pydantic.core import check_dest_ok, check_flags
from argparse_pydantic.test_tools import parsers_actions_diff, parsers_args_equal


class Cfg1(BaseModel):
    arg_1: int
    arg_2: int = 10


class Cfg2(BaseModel):
    arg_3: int = 0


parser_base = argparse.ArgumentParser()
parser_base.add_argument("arg_1", type=int)
parser_base.add_argument("--arg_2", type=int, default=10)
parser_base.add_argument("--arg_3", type=int, default=0)


def test_add_two_models():
    """test add two models"""
    parser = argparse.ArgumentParser()
    add_args_from_model(parser, Cfg1)
    add_args_from_model(parser, Cfg2)
    assert parsers_args_equal(parser_base, parser)
    assert not parsers_actions_diff(parser_base, parser)

    args = parser.parse_args(["10"])
    cfg1 = create_model_obj(Cfg1, args)
    assert cfg1.arg_1 == 10
    assert cfg1 == Cfg1(arg_1=10)
    cfg2 = create_model_obj(Cfg2, args)
    assert cfg2 == Cfg2()

    parser = argparse.ArgumentParser()
    add_args_from_model(parser, [Cfg1, Cfg2])
    assert parsers_args_equal(parser_base, parser)
    assert not parsers_actions_diff(parser_base, parser)


def test_add_model_with_group():
    """add model, create group"""
    parser = argparse.ArgumentParser()
    add_args_from_model(parser, Cfg1, create_group=True)
    assert parser._action_groups[2].title == "Cfg1"
    add_args_from_model(parser, Cfg2, create_group=True)
    assert parser._action_groups[3].title == "Cfg2"


def test_same_args(capsys: CaptureFixture[str]):
    """same args"""
    parser_expected = argparse.ArgumentParser()
    add_args_from_model(parser_expected, [Cfg1, Cfg2])

    parser = argparse.ArgumentParser()
    add_args_from_model(parser, [Cfg1, Cfg2])

    class CfgSamePos(BaseModel):
        arg_1: float

    # same positional, so nothing added
    add_args_from_model(parser, CfgSamePos)
    assert parsers_args_equal(parser_expected, parser)
    assert not parsers_actions_diff(parser_expected, parser)
    captured = capsys.readouterr()
    assert captured.out == "dest arg_1 exists!\n"

    class CfgSamePos2(BaseModel):
        arg_1: float
        arg_4: int

    # same positional, positional not added
    add_args_from_model(parser, CfgSamePos2)
    parser_expected.add_argument("arg_4", type=int)
    assert parsers_args_equal(parser_expected, parser)
    assert not parsers_actions_diff(parser_expected, parser)
    captured = capsys.readouterr()
    assert captured.out == "dest arg_1 exists!\n"

    class CfgSameOpt(BaseModel):
        arg_2: int = 100

    # same optional, so nothing added
    add_args_from_model(parser, CfgSameOpt)
    assert parsers_args_equal(parser_expected, parser)
    assert not parsers_actions_diff(parser_expected, parser)
    captured = capsys.readouterr()
    assert captured.out == "flag ['--arg_2'] exists!\n"

    class CfgSameOpt2(BaseModel):
        arg_2: int = 100
        arg_5: int = 200

    # same optional arg_2,  not added
    add_args_from_model(parser, CfgSameOpt2)
    parser_expected.add_argument("--arg_5", type=int, default=200)
    assert parsers_args_equal(parser_expected, parser)
    assert not parsers_actions_diff(parser_expected, parser)
    captured = capsys.readouterr()
    assert captured.out == "flag ['--arg_2'] exists!\n"

    class CfgOptSameAsPos(BaseModel):
        arg_1: float = 100

    # arg1 optional, but got positional with same name
    add_args_from_model(parser, CfgOptSameAsPos)
    assert parsers_args_equal(parser_expected, parser)
    assert not parsers_actions_diff(parser_expected, parser)
    captured = capsys.readouterr()
    assert captured.out == "flag ['--arg_1'] exists!\n"


def test_check_dest_ok():
    """test check_dest_ok"""
    parser = argparse.ArgumentParser()
    parser.add_argument("arg_1", type=int)
    assert not check_dest_ok("arg_1", parser)
    assert check_dest_ok("arg_2", parser)


def test_check_flags():
    """test check_flags"""
    parser = argparse.ArgumentParser()
    parser.add_argument("arg_1", type=int)
    parser.add_argument("--arg_2", type=int)
    flags = check_flags(["--arg_2"], parser)
    assert not flags
    flags = check_flags(["--arg_1"], parser)
    assert not flags
    flags = check_flags(["--arg_3"], parser)
    assert flags == ["--arg_3"]
    flags = check_flags(["-a", "arg_1"], parser)
    assert not flags
    flags = check_flags([], parser)
    assert not flags
    flags = check_flags(None, parser)
    assert not flags
