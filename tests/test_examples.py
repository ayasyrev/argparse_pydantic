from cli_result.core import Cfg, check_examples


def test_examples() -> None:
    cfg = Cfg(examples_path="examples")
    name = "example_01_simple"
    result = check_examples(cfg, name)
    assert result is None
