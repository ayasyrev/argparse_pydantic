# Example 5 - repeat python docs for argparse example.
# https://docs.python.org/3/library/argparse.html#core-functionality
# Core Functionality
import argparse
from typing import Optional

from pydantic import BaseModel, Field

from argparse_pydantic import add_args_from_model, argument_kwargs, create_model_obj


# Config for our App
class AppCfg(BaseModel):
    filename: str
    count: Optional[str] = Field(
        default=None,
        json_schema_extra=argument_kwargs(
            flag="-c",
        ),
    )  # option that takes a value
    verbose: bool = Field(
        default=False,
        json_schema_extra=argument_kwargs(
            flag="-v", action="store_true"
        ),  # on/off flag
    )


# create parser usual way.
parser = argparse.ArgumentParser(
    prog="ProgramName",
    description="What the program does",
    epilog="Text at the bottom of help",
)


# now we add arguments from config
add_args_from_model(parser, AppCfg)


if __name__ == "__main__":
    # parse arguments.
    # parser return Namespace object
    args = parser.parse_args()
    cfg: AppCfg = create_model_obj(AppCfg, args)
    # now we got object with autocompletion at ide.
    # if you want to play with config at jupyter notebook: import AppCfg.
    print(f"filename={cfg.filename}")
    print(f"count={cfg.count}")
    print(f"verbose={cfg.verbose}")
