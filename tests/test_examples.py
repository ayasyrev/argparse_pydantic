import pytest

from cli_result.core import Cfg, get_examples_names, run_check_example


cfg = Cfg(examples_path="examples")
examples = get_examples_names(cfg=cfg)


@pytest.mark.parametrize("example_name, file_list", examples)
def test_examples(example_name, file_list) -> None:
    result = run_check_example(example_name, file_list, cfg=cfg)
    assert result is None
