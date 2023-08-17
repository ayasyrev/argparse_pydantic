from __future__ import annotations

import argparse
from argparse import ArgumentParser, HelpFormatter
from functools import wraps
from inspect import getdoc, signature
from typing import Any, Callable, List, Optional, Sequence, Type

from pydantic import BaseModel

from argparse_pydantic.core import add_args_from_model, create_model_obj, create_parser
from argparse_pydantic.helpers import ArgumentParserCfg


def get_params(func: Callable[..., Any]) -> List[BaseModel]:
    sig = signature(func)
    params = [
        param.annotation
        for param in sig.parameters.values()
        if issubclass(param.annotation, BaseModel)
    ]
    assert params
    return params


def app(
    parser_cfg: ArgumentParserCfg | None = None,
    prog: str | None = None,
    usage: str | None = None,
    description: str | None = None,
    epilog: str | None = None,
    parents: Sequence[ArgumentParser] = None,
    formatter_class: Type[HelpFormatter] = HelpFormatter,
    prefix_chars: str = "-",
    fromfile_prefix_chars: str | None = None,
    argument_default: str | None = None,
    conflict_handler: str = "error",
    add_help: bool = True,
    allow_abbrev: bool = True,
    exit_on_error: bool = True,
):
    if parents is None:
        parents = []
    if parser_cfg is None:
        parser_cfg = ArgumentParserCfg(
            prog=prog,
            usage=usage,
            description=description,
            epilog=epilog,
            parents=parents,
            formatter_class=formatter_class,
            prefix_chars=prefix_chars,
            fromfile_prefix_chars=fromfile_prefix_chars,
            argument_default=argument_default,
            conflict_handler=conflict_handler,
            add_help=add_help,
            allow_abbrev=allow_abbrev,
            exit_on_error=exit_on_error,
        )
    # """Create app.
    # Simple variant - expecting function with one argument"""

    def create_app(func: Callable[[Type[Any]], None]):
        params = get_params(func)
        app_cfg = params[0]

        @wraps(func)
        def parse_and_run(args: Optional[Sequence[str]] = None) -> None:
            parser = create_parser(parser_cfg)
            add_args_from_model(parser, app_cfg)
            parsed_args = parser.parse_args(args)
            cfg = create_model_obj(app_cfg, parsed_args)
            func(cfg)

        return parse_and_run

    return create_app


class App:
    subparsers: argparse.Action | None = None
    main_func: Callable[[Type[Any]], None]
    commands: dict[str, Callable[[Type[Any]], None]]
    configs: dict[str, Type[Any]]
    main_cfg: BaseModel
    parse_and_run: Callable[[Optional[Sequence[str]]], None]

    def __init__(
        self,
        parser_cfg: ArgumentParserCfg | None = None,
        prog: str | None = None,
        usage: str | None = None,
        description: str | None = None,
        epilog: str | None = None,
        parents: Sequence[ArgumentParser] = None,
        formatter_class: Type[HelpFormatter] = HelpFormatter,
        prefix_chars: str = "-",
        fromfile_prefix_chars: str | None = None,
        argument_default: str | None = None,
        conflict_handler: str = "error",
        add_help: bool = True,
        allow_abbrev: bool = True,
        exit_on_error: bool = True,
    ):
        if parents is None:
            parents = []
        if parser_cfg is None:
            parser_cfg = ArgumentParserCfg(
                prog=prog,
                usage=usage,
                description=description,
                epilog=epilog,
                parents=parents,
                formatter_class=formatter_class,
                prefix_chars=prefix_chars,
                fromfile_prefix_chars=fromfile_prefix_chars,
                argument_default=argument_default,
                conflict_handler=conflict_handler,
                add_help=add_help,
                allow_abbrev=allow_abbrev,
                exit_on_error=exit_on_error,
            )
        self.parser = create_parser(parser_cfg)

    def main(self, func: Callable[[Type[Any]], None]):
        params = get_params(func)
        app_cfg = params[0]
        add_args_from_model(self.parser, app_cfg)
        self.main_func = func
        self.main_cfg = app_cfg

    def command(self, func: Callable[[Type[Any]], None]):
        command_name = func.__name__
        if self.subparsers is None:
            self.subparsers = self.parser.add_subparsers(
                title="Commands", help="Available commands."
            )
            self.commands = {}
            self.configs = {}
        self.commands[command_name] = func
        help = getdoc(func)  # pylint: disable=redefined-builtin
        if help is not None:
            help = help.split("Args", maxsplit=1)[0].strip()
        command_parser = self.subparsers.add_parser(
            command_name,
            help=help,
            description=help,
        )
        command_parser.set_defaults(command=command_name)

        params = get_params(func)
        app_cfg = params[0]
        self.configs[command_name] = app_cfg

        add_args_from_model(command_parser, app_cfg)

    def __call__(self, args: Optional[Sequence[str]] = None) -> None:
        parsed_args = self.parser.parse_args(args)
        if hasattr(parsed_args, "command"):
            cfg = create_model_obj(self.configs[parsed_args.command], parsed_args)
            self.commands[parsed_args.command](cfg)
        else:
            cfg = create_model_obj(self.main_cfg, parsed_args)
            self.main_func(cfg)


def run(
    func: Callable[[Type[Any]], None], parser_cfg: ArgumentParserCfg = None
) -> None:
    """Parse command line arguments and run function"""
    app = App(parser_cfg=parser_cfg)
    app.main(func)
    app()
