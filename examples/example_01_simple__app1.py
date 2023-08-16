# Basic example - create base config for you app with typed config based on pydantic.

from pydantic import BaseModel

from argparse_pydantic.app import app


# Create config for App as BaseModel
class AppCfg(BaseModel):
    arg_1: int = 0
    arg_2: float = 0.1
    arg_3: str = "string"


def my_app(
    cfg: AppCfg,
):
    """Simple app"""
    print(f"arg_1={cfg.arg_1}")
    print(f"arg_2={cfg.arg_2}")
    print(f"arg_3={cfg.arg_3}")


main = app()(my_app)


if __name__ == "__main__":
    main()
