# Basic example - create base config for you app with typed config based on pydantic.
import argparse

from pydantic import BaseModel

from argparse_pydantic import add_args_from_model, create_model_obj


# Create config for App as BaseModel
class AppCfg(BaseModel):
    arg_1: int = 0
    arg_2: float = 0.1
    arg_3: str = "string"


# create argparse.ArgumentParser as usual
parser = argparse.ArgumentParser()
# add arguments to parser from our config
add_args_from_model(parser, AppCfg)


if __name__ == "__main__":
    # parse arguments as usual. We got Namespace without typing
    args_namespace = parser.parse_args()
    # create config object from arguments.
    cfg: AppCfg = create_model_obj(AppCfg, args_namespace)  # type: ignore
    # now we got object with autocompletion at ide.
    # if you want to play with config at jupyter notebook: import AppCfg.
    print(f"arg_1={cfg.arg_1}")
    print(f"arg_2={cfg.arg_2}")
    print(f"arg_3={cfg.arg_3}")
