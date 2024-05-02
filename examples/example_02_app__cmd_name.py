# Basic example - create base config for you app with typed config based on pydantic.
from pydantic import BaseModel

from argparse_pydantic.app import App

app = App()


# Create config for App as BaseModel
class AppCfg(BaseModel):
    arg_1: int = 0
    arg_2: float = 0.1
    arg_3: str = "string"


@app.main
def my_app(
    cfg: AppCfg,
):
    """Simple app"""
    print(f"arg_1={cfg.arg_1}")
    print(f"arg_2={cfg.arg_2}")
    print(f"arg_3={cfg.arg_3}")


class CmdCfg(BaseModel):
    cmd_1: int = 0
    verbose: bool = False


@app.command("cmd")  # or @app.command(name="cmd")
def cmd_func(
    cfg: CmdCfg,
):
    """Command - simple command func"""
    print(f"cmd_1={cfg.cmd_1}")
    print(f"verbose={cfg.verbose}")


if __name__ == "__main__":
    app()
