from pathlib import Path

import nox

example_files = list(Path("examples").glob("example*.py"))
print(f"examples files: {', '.join(file.name for file in example_files)}")


@nox.session(python=["3.8", "3.9", "3.10", "3.11", "3.12"], venv_backend="mamba")
def tests_examples(session: nox.Session) -> None:
    session.install(".")
    for filename in example_files:
        session.run("python", str(filename))
