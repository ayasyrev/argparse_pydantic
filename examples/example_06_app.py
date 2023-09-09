# App with several configs.
from pydantic import BaseModel

from argparse_pydantic import App


class AppCfg(BaseModel):
    arg_1: int = 0
    arg_2: float = 0.1
    arg_3: str = "string"


class DataCfg(BaseModel):
    data_1: str = "data_1"
    data_2: int = 1


class CmdCfg(BaseModel):
    cmd_1: int = 0
    verbose: bool = False


class CmdCfg2(BaseModel):
    cmd_2: int = 0
    force: bool = False


app = App(
    prog="example_app",
    group_cfgs=True,
)


@app.main
def my_app(
    cfg: AppCfg,
    data_cfg: DataCfg,
):
    """Simple app"""
    print(f"arg_1={cfg.arg_1}")
    print(f"arg_2={cfg.arg_2}")
    print(f"arg_3={cfg.arg_3}")
    print(f"data_1={data_cfg.data_1}")
    print(f"data_2={data_cfg.data_2}")


@app.command
def cmd(
    cfg: CmdCfg,
    cfg2: CmdCfg2,
):
    """Command - simple command func"""
    print(f"cmd_1={cfg.cmd_1}")
    print(f"verbose={cfg.verbose}")
    print(f"cmd_2={cfg2.cmd_2}")
    print(f"force={cfg2.force}")


if __name__ == "__main__":
    app()
