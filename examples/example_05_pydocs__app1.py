# Example 5 - repeat python docs for argparse example.
# https://docs.python.org/3/library/argparse.html#core-functionality
# Core Functionality
from typing import Optional

from pydantic import BaseModel, Field

from argparse_pydantic import argument_kwargs
from argparse_pydantic.app import app


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


# create app.
# arguments as argparse.ArgumentParser
@app(
    prog="ProgramName",
    description="What the program does",
    epilog="Text at the bottom of help",
)
def my_app(
    cfg: AppCfg,
):
    """Simple app"""
    print(f"filename={cfg.filename}")
    print(f"count={cfg.count}")
    print(f"verbose={cfg.verbose}")


if __name__ == "__main__":
    my_app()
