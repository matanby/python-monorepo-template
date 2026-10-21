# <SERVICE-NAME>

Requires uv and Python 3.12+. Run `uv lock` at the repository root after creation,
then `make install` here (or `uv sync --all-packages --locked` at the root).

- `make test`: test this service.
- `make lint`: check code with Ruff.
- `make format`: format code with Ruff.
- `make run`: run the installed service entry point.
- `make docker-build`: build from the repository root context, including workspace packages.
- `make docker-run`: run the image.
- `make typecheck`: check Python types with ty.
