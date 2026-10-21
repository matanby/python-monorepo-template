"""Exercise generated projects, installed wheels, and optionally their production image."""

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LIBRARY = "template-smoke-library"
SERVICE = "template-smoke-service"
GREETING = f"Hello from {SERVICE}!"


def run(arguments: list[str], root: Path) -> str:
    # Nested uv commands must use the temporary workspace's environment.
    environment = os.environ.copy()
    environment.pop("VIRTUAL_ENV", None)
    environment.pop("UV_PROJECT_ENVIRONMENT", None)
    print(f"Running: {' '.join(arguments)}", flush=True)
    result = subprocess.run(
        arguments,
        cwd=root,
        env=environment,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
    )
    print(result.stdout, end="", flush=True)
    result.check_returncode()
    return result.stdout


def smoke(root: Path, *, docker: bool = False) -> None:
    for file in (
        "pyproject.toml",
        "uv.lock",
        ".python-version",
        ".dockerignore",
        ".gitignore",
        "LICENSE",
        "Makefile",
    ):
        shutil.copy2(ROOT / file, root / file)
    for folder in ("scripts", "templates", "tests"):
        shutil.copytree(
            ROOT / folder,
            root / folder,
            ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache", ".ruff_cache", ".venv"),
        )
    for folder in ("services", "packages"):
        (root / folder).mkdir()
    for kind, name in (("package", LIBRARY), ("service", SERVICE)):
        run([sys.executable, "scripts/scaffold.py", kind, name], root)
    library_source = root / "packages" / LIBRARY / "src/template_smoke_library/__init__.py"
    greeting_code = f'def greeting() -> str:\n    return "{GREETING}"\n'
    library_source.write_text(greeting_code, encoding="utf-8")
    service_source = root / "services" / SERVICE / "src/template_smoke_service/__main__.py"
    service_source.write_text(
        "from template_smoke_library import greeting\n\n\n"
        "def main() -> None:\n    print(greeting())\n\n\n"
        'if __name__ == "__main__":\n    main()\n',
        encoding="utf-8",
    )
    run(["uv", "add", "--package", SERVICE, "--workspace", LIBRARY], root)
    run(["uv", "sync", "--all-packages", "--locked"], root)
    run(["uv", "run", "--all-packages", "--locked", "ruff", "check", "."], root)
    run(
        ["uv", "run", "--all-packages", "--locked", "ruff", "format", "--check", "--diff", "."],
        root,
    )
    run(["uv", "run", "--all-packages", "--locked", "ty", "check"], root)
    run(["uv", "run", "--all-packages", "--locked", "python", "scripts/test_all.py"], root)
    output = run(["uv", "run", "--locked", "--package", SERVICE, SERVICE], root)
    if output.strip() != GREETING:
        raise RuntimeError("The service did not return the expected greeting.")
    run(["uv", "build", "--all-packages", "--out-dir", "dist"], root)
    # Install built distributions in a fresh environment with no source path or dev dependencies.
    runtime = root / "wheel-runtime"
    run(["uv", "venv", str(runtime)], root)
    python = runtime / ("Scripts/python.exe" if sys.platform == "win32" else "bin/python")
    wheels = sorted(str(path) for path in (root / "dist").glob("*.whl"))
    if len(wheels) != 2:
        raise RuntimeError(f"Expected two generated wheels, found {len(wheels)}.")
    run(["uv", "pip", "install", "--python", str(python), "--no-deps", *wheels], root)
    probe = f"""
from importlib.metadata import distribution
from importlib.resources import files
from template_smoke_service.__main__ import main
for name in ("template_smoke_library", "template_smoke_service"):
    assert files(name).joinpath("py.typed").is_file(), name
metadata = distribution("{SERVICE}")
assert any(req.startswith("{LIBRARY}") for req in metadata.requires or [])
assert all("file:" not in req for req in metadata.requires or [])
assert any("LICENSE" in str(file) for file in metadata.files or [])
main()
"""
    output = run([str(python), "-I", "-c", probe], root)
    if output.strip() != GREETING:
        raise RuntimeError("The installed wheels did not return the expected greeting.")
    if docker:
        tag = "monorepo-template-smoke:local"
        build = ["docker", "build", "-t", tag, "-f", f"services/{SERVICE}/Dockerfile"]
        # The CA is mounted only for the build and is never copied into the image.
        certificate = os.environ.get("CODEX_PROXY_CERT")
        if certificate:
            build.extend(["--secret", f"id=proxy_ca,src={certificate}"])
        run([*build, "."], root)
        output = run(["docker", "run", "--rm", "--init", tag], root)
        if output.strip() != GREETING:
            raise RuntimeError("The Docker service did not return the expected greeting.")
        run(
            [
                "docker",
                "run",
                "--rm",
                tag,
                "python",
                "-I",
                "-c",
                "import os; from importlib.util import find_spec; "
                "assert os.getuid() == 10001; assert find_spec('pytest') is None",
            ],
            root,
        )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--docker", action="store_true", help="Build and run the service image")
    args = parser.parse_args()
    with tempfile.TemporaryDirectory(prefix="monorepo-smoke-") as temporary:
        smoke(Path(temporary), docker=args.docker)
    print("Smoke checks passed.")


if __name__ == "__main__":
    main()
