import argparse

from argparse_pydantic.test_tools import (
    actions_diff,
    actions_equal,
    actions_same,
    parsers_actions_diff,
    parsers_actions_equal,
    parsers_args_equal,
    parsers_equal,
    parsers_equal_typed,
)


def test_args_equal():
    """test parsers_args_equal"""
    parser_1 = argparse.ArgumentParser()
    parser_2 = argparse.ArgumentParser()
    assert parsers_args_equal(parser_1, parser_2)
    parser_2 = argparse.ArgumentParser(prog="test_name")
    assert not parsers_args_equal(parser_1, parser_2)


def test_parsers_actions_equal():
    """test parsers_actions_equal"""
    parser_1 = argparse.ArgumentParser()
    parser_2 = argparse.ArgumentParser()
    # initial - only help action
    assert parsers_actions_equal(parser_1, parser_2)
    # different len
    parser_1.add_argument("arg1")
    assert not parsers_actions_equal(parser_1, parser_2)
    # again the same
    parser_2.add_argument("arg1")
    assert parsers_actions_equal(parser_1, parser_2)
    # different args
    parser_1.add_argument("arg2")
    parser_2.add_argument("arg3")
    assert not parsers_actions_equal(parser_1, parser_2)


def tests_actions_equal_diff():
    """test actions_diff"""
    # pylint: disable=protected-access
    parser_1 = argparse.ArgumentParser()
    parser_2 = argparse.ArgumentParser()
    parser_1.add_argument("arg1")
    parser_2.add_argument("arg1")
    action_1 = parser_1._actions[1]
    action_2 = parser_2._actions[1]
    assert actions_equal(action_1, action_2)
    assert actions_diff(action_1, action_2) == {}

    # same actions, different args
    parser_2 = argparse.ArgumentParser()
    parser_2.add_argument("arg1", default=1)
    action_2 = parser_2._actions[1]
    assert actions_same(action_1, action_2)
    assert not actions_equal(action_1, action_2)
    assert actions_diff(action_1, action_2) == {"default": (None, 1)}

    # different actions
    parser_2 = argparse.ArgumentParser()
    parser_2.add_argument("arg1", action="store_true")
    action_2 = parser_2._actions[1]
    assert not actions_same(action_1, action_2)
    assert not actions_equal(action_1, action_2)
    assert actions_diff(action_1, action_2) == {}


def tests_parsers_actions_diff():
    """test parsers_diff"""
    parser_1 = argparse.ArgumentParser()
    parser_2 = argparse.ArgumentParser()
    parser_1.add_argument("arg1")
    parser_2.add_argument("arg1")
    assert not parsers_actions_diff(parser_1, parser_2)

    # # same actions, different args
    parser_2 = argparse.ArgumentParser()
    parser_2.add_argument("arg1", default=1)
    expected = [{"default": (None, 1)}]
    assert parsers_actions_diff(parser_1, parser_2) == expected

    # # different actions
    parser_2 = argparse.ArgumentParser()
    parser_2.add_argument("arg1", action="store_true")
    # pylint: disable=protected-access
    expected = [{"action_type": (argparse._StoreAction, argparse._StoreTrueAction)}]  # type: ignore
    assert parsers_actions_diff(parser_1, parser_2) == expected


def test_parsers_equal():
    """test parsers_equal"""
    parser_1 = argparse.ArgumentParser()
    parser_2 = argparse.ArgumentParser()
    assert parsers_equal(parser_1, parser_2)
    parser_1.add_argument("arg1")
    assert not parsers_equal(parser_1, parser_2)
    parser_2.add_argument("arg1")
    assert parsers_equal(parser_1, parser_2)


def test_parsers_equal_typed():
    """test parsers_equal"""
    parser_1 = argparse.ArgumentParser()
    parser_2 = argparse.ArgumentParser()
    parser_1.add_argument("arg1")
    parser_2.add_argument("arg1", type=str)
    assert not parsers_equal(parser_1, parser_2)
    diff = parsers_actions_diff(parser_1, parser_2)
    assert diff == [{"type": (None, str)}]
    assert parsers_equal_typed(parser_1, parser_2)
