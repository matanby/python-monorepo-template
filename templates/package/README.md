# <PACKAGE-NAME>

Requires uv and Python 3.12+. Run `uv lock` at the repository root after creation,
then `make install` here (or `uv sync --all-packages --locked` at the root).

- `make test`: test this package.
- `make lint`: check code with Ruff.
- `make format`: format code with Ruff.
- `make typecheck`: check Python types with ty.
