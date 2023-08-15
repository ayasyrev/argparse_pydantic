from cli_result.core import Cfg, check_examples


example_list = [  # will be removed -> all examples
    "example_01_simple",
    "example_03_help",
]


def test_examples() -> None:
    cfg = Cfg(examples_path="examples")
    result = check_examples(cfg, example_list)
    assert result is None
