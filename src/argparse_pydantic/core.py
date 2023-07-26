from __future__ import annotations

import argparse
from typing import Any, Iterable, Optional, Sequence, Type, Union

from pydantic import BaseModel
from pydantic.fields import FieldInfo
from pydantic_core import PydanticUndefined
from typing_extensions import get_args, get_origin

from argparse_pydantic.helpers import ArgumentParserCfg, create_parser

ArgType = Union[str, argparse.FileType, type, None]

ARG_KEYWORDS = (
    "action",
    "action",
    "nargs",
    "const",
    "default",
    "type",
    "choices",
    "required",
    "help",
    "metavar",
    "dest",
    "version",
    # not in argparse, for flags
    "flag",
    "positional",
)


def argument_kwargs(
    flag: str | None = None,
    action: str | None = None,
    nargs: int | str | None = None,
    const: str | None = None,
    default: Any = None,
    type: ArgType = None,  # pylint: disable=redefined-builtin
    choices: Iterable[Any] | None = None,
    required: bool | None = None,
    help: str | None = None,  # pylint: disable=redefined-builtin
    metavar: str | tuple[str, ...] | None = None,
    dest: str | None = None,
    positional: bool | None = None,
) -> dict[str, Any]:
    """create dict with args for argparse.add_argument"""
    if default is PydanticUndefined:
        default = None
    kwargs = {
        "flag": flag,
        "action": action,
        "nargs": nargs,
        "const": const,
        "default": default,
        "type": type,
        "choices": choices,
        "required": required,
        "help": help,
        "metavar": metavar,
        "dest": dest,
        "positional": positional,
    }
    return {key: val for key, val in kwargs.items() if val is not None}


def get_field_type(field_info: FieldInfo) -> Type:
    """get field type, convert to base type."""
    field_type = field_info.annotation
    if get_origin(field_type) is Union:
        return get_args(field_type)[0]
    return field_type


def parse_field_kwargs(json_schema_extra: dict[str, Any]) -> dict[str, Any]:
    """parse json_schema_extra for argparse add_argument args"""
    field_kwargs = {key: val for key, val in json_schema_extra.items() if key in ARG_KEYWORDS and val is not None}
    if "flag" in field_kwargs:
        field_kwargs["flag"] = process_flag(field_kwargs["flag"])
    return field_kwargs


def add_field_arg(
    parser: argparse.ArgumentParser, field_name: str, field_info: FieldInfo
) -> None:
    """add argument to parser from field_info"""
    flags = [f"--{field_name}"]
    kwargs = argument_kwargs(
        help=field_info.description,
        required=field_info.is_required(),
        default=field_info.default if field_info.default is not PydanticUndefined else None,
        type=get_field_type(field_info),
    )

    if field_info.json_schema_extra:
        field_kwargs = parse_field_kwargs(field_info.json_schema_extra)
        kwargs = {
            **field_kwargs,
            **kwargs,
        }

    if "flag" in kwargs:
        flags.insert(0, kwargs.pop("flag"))

    if field_info.default is PydanticUndefined:
        if kwargs.pop("positional", False):
            kwargs["dest"] = field_name
            flags = []
            kwargs.pop("required", None)
        else:
            kwargs["required"] = True

    if "action" in kwargs:
        kwargs.pop("type", None)
        validate_action(kwargs["action"], kwargs.get("default", None))
        if kwargs["action"] not in ("count", "store_const"):
            kwargs.pop("default", None)

    # process help message - ? add additional info like defaults and type
    parser.add_argument(*flags, **kwargs)


def process_flag(flag) -> Optional[str]:
    """check short flag - if without prefix - add it, if long string, return None"""
    if len(flag) == 1:
        return f"-{flag}"
    if flag.startswith("-") and len(flag) == 2:
        return flag
    return None


def validate_action(action: str, default: Optional[Type]) -> None:
    """Check if store true / false corresponds to default value"""
    if action in ("store_true", "store_false"):
        action_default = action.split("_")[1]
        if action_default == str(default).lower():
            raise ValueError(f"action {action} doesn't match default {default}")


def add_args_from_model(
    parser: argparse.ArgumentParser, model: BaseModel
) -> argparse.ArgumentParser:
    """add args from model to parser"""
    for field_name, field_info in model.model_fields.items():
        add_field_arg(parser, field_name, field_info)
    return parser


def create_model_obj(model: BaseModel, args: argparse.Namespace) -> BaseModel:
    """create model from parsed args"""
    kwargs = {
        key: val for key, val in args.__dict__.items() if key in model.model_fields
    }
    return model(**kwargs)


def parse_args(
    cfg: Type[BaseModel],
    parser_cfg: ArgumentParserCfg | None = None,
    args: Sequence[str] | None = None,
) -> BaseModel:
    """parse args"""
    parser = create_parser(parser_cfg)
    add_args_from_model(parser, cfg)
    parsed_args = parser.parse_args(args=args)
    return create_model_obj(cfg, parsed_args)
