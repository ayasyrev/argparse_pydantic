# Example 3 - create config with helps.
from pydantic import BaseModel, Field

from argparse_pydantic import ArgumentParserCfg, argument_kwargs
from argparse_pydantic.app import run


# Create config for parser
parser_cfg = ArgumentParserCfg(
    prog="name", description="example prog", epilog="nothing done, just example..."
)


# Create config for App
class AppCfg(BaseModel):
    arg_1: int = Field(
        default=0,
        # add help
        description="argument 1, int",
    )
    arg_2: str = Field(
        default="",
        # short flag can be add as json_schema_extra
        json_schema_extra={"flag": "s"},
        description="string arg, can be used with short flag -s",
    )
    arg_3: float = Field(
        default=0.0,
        json_schema_extra=argument_kwargs(flag="f"),
    )


def my_app(
    cfg: AppCfg,
):
    """Simple app"""
    print(f"arg_1={cfg.arg_1}")
    print(f"arg_2={cfg.arg_2}")
    print(f"arg_3={cfg.arg_3}")


if __name__ == "__main__":
    run(my_app, parser_cfg=parser_cfg)
