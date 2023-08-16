from cli_result.core import Cfg, check_examples


def test_examples() -> None:
    cfg = Cfg(examples_path="examples")
    result = check_examples(cfg=cfg)
    assert result is None
