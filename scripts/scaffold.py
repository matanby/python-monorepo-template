"""Create workspace members without platform-specific shell substitutions."""

import argparse
import keyword
import re
import shutil
import sys
import tempfile
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def create(kind: str, name: str, root: Path = ROOT) -> Path:
    if kind not in {"package", "service"}:
        raise ValueError("Expected package or service.")
    if not re.fullmatch(r"[a-z][a-z0-9]*(?:[-_][a-z0-9]+)*", name):
        raise ValueError(
            "Use a lowercase name starting with a letter, with hyphens or underscores."
        )
    module = name.replace("-", "_")
    if keyword.iskeyword(module) or keyword.issoftkeyword(module):
        raise ValueError("The name must not be a Python keyword.")
    if module in sys.stdlib_module_names:
        raise ValueError("The import name must not shadow a Python standard library module.")
    canonical = name.replace("_", "-")
    for folder in ("services", "packages"):
        for existing in (root / folder).iterdir():
            names = [existing.name]
            metadata = existing / "pyproject.toml"
            if metadata.is_file():
                project = tomllib.loads(metadata.read_text(encoding="utf-8")).get("project", {})
                names.append(project.get("name", existing.name))
            if any(re.sub(r"[-_.]+", "-", value).lower() == canonical for value in names):
                raise ValueError(f"A workspace member already exists: {existing.name}")
    destination = root / f"{kind}s" / name
    # Stage the complete result so a failed render cannot leave a partial project.
    with tempfile.TemporaryDirectory(dir=root) as staging:
        staged = Path(staging) / name
        shutil.copytree(
            root / "templates" / kind,
            staged,
            ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache", ".ruff_cache", ".venv"),
        )
        (staged / "src" / f"{kind}_name").rename(staged / "src" / module)
        for path in staged.rglob("*"):
            if path.is_file():
                content = path.read_text(encoding="utf-8")
                content = content.replace(f"<{kind.upper()}-NAME>", name)
                content = content.replace(f"<{kind.upper()}_NAME>", module)
                content = content.replace(f"{kind}_name", module)
                path.write_text(content, encoding="utf-8", newline="\n")
        staged.rename(destination)
    return destination


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("kind", choices=("package", "service"))
    parser.add_argument("name")
    args = parser.parse_args()
    try:
        destination = create(args.kind, args.name)
    except ValueError as error:
        parser.error(str(error))
    print(f"Created {destination.relative_to(ROOT)}. Run uv lock, then uv sync --all-packages.")


if __name__ == "__main__":
    main()
