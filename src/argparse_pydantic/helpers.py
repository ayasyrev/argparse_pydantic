import argparse
import sys
from typing import Optional, Sequence, Type

from pydantic import BaseModel, ConfigDict, Field


class ArgumentParserCfg(BaseModel):
    """Config schema for argparse parser.
    Parameters same as at argparse.ArgumentParser.
    """
    prog: Optional[str] = None
    usage: Optional[str] = None
    description: Optional[str] = None
    epilog: Optional[str] = None
    parents: Sequence[argparse.ArgumentParser] = Field(default_factory=list)
    formatter_class: Type[argparse.HelpFormatter] = argparse.HelpFormatter
    prefix_chars: str = "-"
    fromfile_prefix_chars: Optional[str] = None
    argument_default: Optional[str] = None
    conflict_handler: str = "error"
    add_help: bool = True
    allow_abbrev: bool = True
    exit_on_error: bool = True

    model_config = ConfigDict(arbitrary_types_allowed=True)


def create_parser(
    parser_cfg: Optional[ArgumentParserCfg] = None,
) -> argparse.ArgumentParser:
    """Create argparse parser."""
    if parser_cfg is None:
        parser_cfg = ArgumentParserCfg()
    kwargs = parser_cfg.model_dump(exclude_none=True)
    if sys.version_info.minor < 9:  # from python 3.9
        kwargs.pop("exit_on_error")  # pragma: no cover
    parser = argparse.ArgumentParser(**kwargs)
    return parser
