"""Run each project's tests separately to avoid module and configuration collisions."""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    projects = [ROOT]
    for folder in ("packages", "services"):
        projects.extend(sorted(path.parent for path in (ROOT / folder).glob("*/pyproject.toml")))
    for project in projects:
        print(f"Testing {project.relative_to(ROOT)}", flush=True)
        subprocess.run(
            [sys.executable, "-m", "pytest", "tests", *sys.argv[1:]],
            cwd=project,
            check=True,
        )


if __name__ == "__main__":
    main()
