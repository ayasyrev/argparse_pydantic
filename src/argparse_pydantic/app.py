from __future__ import annotations

import argparse
from argparse import ArgumentParser, HelpFormatter
from functools import partial, wraps
from inspect import getdoc, signature
from typing import Any, Callable, List, NamedTuple, Optional, Sequence, Tuple, Type

from pydantic import BaseModel

from argparse_pydantic.core import add_args_from_model, create_model_obj, create_parser
from argparse_pydantic.helpers import ArgumentParserCfg


class Arg(NamedTuple):
    name: str
    model: BaseModel


def get_args(func: Callable[..., Any]) -> List[Arg]:
    """process func parameters, return tuple (name, BaseModel)"""
    sig = signature(func)
    params = [
        Arg(param.name, param.annotation)
        for param in sig.parameters.values()
        if issubclass(param.annotation, BaseModel)
    ]
    assert params
    return params


def get_models(args: List[Arg]) -> List[BaseModel]:
    """get list models from args"""
    return [arg.model for arg in args]


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
    """create app from function"""
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

    # Create app.
    # Simple variant - expecting function with one argument.
    def create_app(func: Callable[[Type[Any]], None]):
        args = get_args(func)
        app_cfg = args[0].model

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
        group_cfgs: bool = False,
    ):
        if parents is None:
            parents = []
        self.parser_cfg = parser_cfg or ArgumentParserCfg(
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
        self.commands: dict[str, Callable[[Type[Any]], None]] = {}
        self.configs: dict[str, List[Arg]] = {}
        self.group_cfgs = group_cfgs

    def main(self, func: Callable[[Type[Any]], None]):
        self.commands["main"] = func
        self.configs["main"] = get_args(func)

    def command(self, func: Callable[[Type[Any]], None] = None, *, name: str = ""):
        if func is None:
            return partial(self.command, name=name)
        if isinstance(func, str):
            return partial(self.command, name=func)

        self.commands[name or func.__name__] = func
        self.configs[name or func.__name__] = get_args(func)

    def __call__(self, args: Optional[Sequence[str]] = None) -> None:
        parser = create_parser(self.parser_cfg)
        if len(self.commands) == 1:
            if not hasattr(self.commands, "main"):
                command_name = next(iter(self.commands))
                main_cmd = self.commands.pop(command_name)
                self.commands["main"] = main_cmd
                self.configs["main"] = self.configs.pop(command_name)
        add_args_from_model(parser, get_models(self.configs["main"]), create_group=self.group_cfgs)
        if len(self.commands) > 1:
            subparsers = parser.add_subparsers(
                title="Commands", help="Available commands."
            )
            commands = [name for name in self.commands if name != "main"]
            for command_name in commands:
                cmd_help = getdoc(self.commands[command_name])
                if cmd_help is not None:
                    cmd_help = cmd_help.split("Args", maxsplit=1)[0].strip()
                command_parser = subparsers.add_parser(
                    command_name,
                    help=cmd_help,
                    description=cmd_help,
                )
                command_parser.set_defaults(command=command_name)
                add_args_from_model(
                    command_parser,
                    get_models(self.configs[command_name]),
                    create_group=self.group_cfgs,
                )

        parsed_args = parser.parse_args(args)
        command = getattr(parsed_args, "command", "main")
        cfgs = {
            name: create_model_obj(model, parsed_args)
            for name, model in self.configs[command]
        }
        self.commands[command](**cfgs)


def run(
    func: Callable[[BaseModel], None],
    *args: Callable[[BaseModel], None],
    **kwargs: Callable[[BaseModel], None],
) -> None:
    """Parse command line arguments and run function.
    Pass ArgumentParser Cfg as `parser_cfg=parser_cfg`.
    Pass command functions as arguments or `command=func`."""
    parser_cfg = kwargs.pop("parser_cfg", None)
    run_app = App(parser_cfg=parser_cfg)
    run_app.main(func)
    if args:
        for arg in args:
            run_app.command(arg)
    for command_name, cmd_func in kwargs.items():
        run_app.command(cmd_func, name=command_name)
    run_app()
