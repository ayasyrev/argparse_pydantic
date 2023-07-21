from __future__ import annotations

import argparse
from typing import Any, Iterable, Sequence, Type, Union

from pydantic import BaseModel
from pydantic.fields import FieldInfo
from pydantic_core import PydanticUndefined

from argparse_pydantic.helpers import ArgumentParserCfg, create_parser

ArgType = Union[str, argparse.FileType, type, None]


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


def add_field_arg(
    parser: argparse.ArgumentParser, field_name: str, field_info: FieldInfo
) -> None:
    help_message = field_info.description
    flags = []
    dest = None
    positional = None
    required = field_info.is_required()

    if field_info.json_schema_extra:
        flag = field_info.json_schema_extra.get("flag", None)
        if flag:
            if len(flag) == 1:
                flags.insert(0, f"-{flag}")
            if flag.startswith("-") and len(flag) == 2:
                flags.insert(0, flag)
        help_message = field_info.json_schema_extra.get("help", help_message)
        positional = field_info.json_schema_extra.get("positional", None)

    if field_info.default is PydanticUndefined:
        if positional:
            dest = field_name
            flags = []
        else:
            required = True
    flags.append(f"--{field_name}")

    # process help message - ? add additional info like defaults and type
    kwargs = argument_kwargs(
        default=field_info.default,
        type=field_info.annotation,
        required=required,
        help=help_message,
        dest=dest,
    )
    parser.add_argument(*flags, **kwargs)


def add_args_from_model(
    parser: argparse.ArgumentParser, model: BaseModel
) -> argparse.ArgumentParser:
    for field_name, field_info in model.model_fields.items():
        add_field_arg(parser, field_name, field_info)
    return parser


def create_model_obj(model: BaseModel, args: argparse.Namespace) -> BaseModel:
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
