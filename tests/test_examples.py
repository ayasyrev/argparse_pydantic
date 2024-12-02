import pytest
from cli_result.core import Cfg, get_examples, run_check_example

cfg = Cfg(examples_path="examples")
examples = get_examples(cfg=cfg)


@pytest.mark.parametrize("example_name, file_list", examples)
def test_examples(example_name, file_list) -> None:
    result = run_check_example(example_name, file_list, cfg=cfg)
    assert result is None, (
        "result:\n" f"{result[0].res}" "---\n" "expected:\n" f"{result[0].exp}" "---\n"
    )
