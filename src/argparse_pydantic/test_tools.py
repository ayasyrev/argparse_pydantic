from __future__ import annotations

import argparse
from typing import Any


def parsers_args_equal(
    parser_1: argparse.ArgumentParser,
    parser_2: argparse.ArgumentParser,
) -> bool:
    """compare two parsers, return True if equal."""
    for attr in parser_1.__dict__:
        if not attr.startswith("_"):
            if getattr(parser_1, attr) != getattr(parser_2, attr):
                return False
    return True


def actions_same(action1: argparse.Action, action2: argparse.Action) -> bool:
    return isinstance(action1, type(action2))


def actions_equal(action1: argparse.Action, action2: argparse.Action) -> bool:
    """Compare actions at two parsers"""
    if not actions_same(action1, action2):
        return False
    return all(
        val == action2.__dict__[key]
        for key, val in action1.__dict__.items()
        if key != "container"
    )


def actions_diff(
    action1: argparse.Action, action2: argparse.Action
) -> dict[str, tuple[Any, Any]]:
    """Compare actions at two parsers"""
    if actions_same(action1, action2):
        return {
            key: (val, action2.__dict__[key])
            for key, val in action1.__dict__.items()
            if key != "container" and val != action2.__dict__[key]
        }
    else:
        return {}


def parsers_actions_equal(
    parser_1: argparse.ArgumentParser,
    parser_2: argparse.ArgumentParser,
) -> bool:
    """Compare actions at two parsers.
    Parsers equal if same actions and same order."""
    # if same args but different order will be False - need another check
    # pylint: disable=protected-access
    actions_1 = parser_1._actions
    actions_2 = parser_2._actions
    if len(actions_1) != len(actions_2):
        return False
    for act_1, act_2 in zip(actions_1, actions_2):
        if not actions_equal(act_1, act_2):
            return False
    return True


def parsers_actions_diff(
    parser_1: argparse.ArgumentParser,
    parser_2: argparse.ArgumentParser,
) -> list[dict[str, tuple[Any, Any]]]:
    """Compare actions at two parsers"""
    actions_1 = parser_1._actions  # pylint: disable=protected-access
    actions_2 = parser_2._actions  # pylint: disable=protected-access
    res: list[dict[str, tuple[Any, Any]]] = []
    for act_1, act_2 in zip(actions_1, actions_2):
        if not actions_same(act_1, act_2):
            res.append({"action_type": (type(act_1), type(act_2))})
        else:
            if not actions_equal(act_1, act_2):
                res.append(actions_diff(act_1, act_2))
    return res


def parsers_equal(
    parser_1: argparse.ArgumentParser,
    parser_2: argparse.ArgumentParser,
) -> bool:
    """Compare two parsers"""
    return parsers_args_equal(parser_1, parser_2) and parsers_actions_equal(
        parser_1, parser_2
    )


def parsers_equal_typed(
    parser_1: argparse.ArgumentParser,
    parser_2: argparse.ArgumentParser,
) -> bool:
    """Compare two parsers, dont care type None vs str"""
    diff = parsers_actions_diff(parser_1, parser_2)
    if len(diff) > 0:
        for item in diff.copy():
            types_tuple = item.get("type", None)
            if types_tuple in ((str, None), (None, str)):
                diff.remove(item)
    return len(diff) == 0
