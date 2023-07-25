from typing import Optional
from pydantic import BaseModel
from pydantic_core import PydanticUndefined

from argparse_pydantic.core import argument_kwargs, get_field_type, process_flag


def test_argument_kwargs():
    """test argument kwargs"""
    assert argument_kwargs() == {}

    class Model(BaseModel):
        arg_int: int

    field = Model.model_fields["arg_int"]
    assert field.default == PydanticUndefined
    assert argument_kwargs(default=field.default) == {}


def test_get_field_type():
    """test get_field_type"""

    class Model(BaseModel):
        arg_1: int
        arg_2: Optional[int] = None

    assert get_field_type(Model.model_fields["arg_1"]) == int
    assert Model.model_fields["arg_2"].annotation == Optional[int]
    assert get_field_type(Model.model_fields["arg_2"]) == int


def test_process_flag():
    """test process_flag"""
    assert process_flag("a") == "-a"
    assert process_flag("-a") == "-a"
    assert process_flag("--a") is None
