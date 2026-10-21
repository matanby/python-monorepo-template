import importlib.util
import os
import shutil
import subprocess
import sys
import tempfile
import tomllib
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("scaffold", ROOT / "scripts/scaffold.py")
assert SPEC is not None and SPEC.loader is not None
scaffold = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(scaffold)


class ScaffoldTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="template test ")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        shutil.copytree(ROOT / "templates", self.root / "templates")
        for folder in ("services", "packages"):
            (self.root / folder).mkdir()

    def test_generated_projects(self) -> None:
        for kind in ("package", "service"):
            with self.subTest(kind=kind):
                name = f"hello-{kind}"
                module = name.replace("-", "_")
                project = scaffold.create(kind, name, self.root)
                metadata = tomllib.loads((project / "pyproject.toml").read_text(encoding="utf-8"))
                self.assertEqual(metadata["project"]["name"], name)
                self.assertTrue((project / "src" / module / "__init__.py").is_file())
                self.assertTrue((project / "src" / module / "py.typed").is_file())
                self.assertEqual(
                    (project / "LICENSE").read_text(encoding="utf-8"),
                    (ROOT / "LICENSE").read_text(encoding="utf-8"),
                )
                for path in project.rglob("*"):
                    if path.is_file():
                        content = path.read_text(encoding="utf-8")
                        self.assertNotIn(f"<{kind.upper()}", content)
                        self.assertNotIn(f"{kind}_name", content)
                        self.assertNotIn(b"\r\n", path.read_bytes())
                environment = os.environ.copy()
                environment["PYTHONPATH"] = str(project / "src")
                subprocess.run(
                    [sys.executable, "-m", "unittest", "discover", "-s", "tests"],
                    cwd=project,
                    env=environment,
                    capture_output=True,
                    check=True,
                )
                if kind == "service":
                    result = subprocess.run(
                        [sys.executable, str(project / "src" / module / "__main__.py")],
                        check=True,
                        text=True,
                        capture_output=True,
                    )
                    self.assertEqual(result.stdout, f"Hello from {name}!\n")

    def test_invalid_names_leave_repository_untouched(self) -> None:
        for name in ("", "../escape", "123", "Upper", "has space", "a--b", "class", "logging"):
            with self.subTest(name=name), self.assertRaises(ValueError):
                scaffold.create("package", name, self.root)
        self.assertEqual(list((self.root / "packages").iterdir()), [])

    def test_invalid_kind_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            scaffold.create("../escape", "valid-name", self.root)

    def test_normalized_collision_does_not_overwrite(self) -> None:
        original = scaffold.create("package", "shared-utils", self.root)
        marker = original / "keep.txt"
        marker.write_text("keep me", encoding="utf-8")
        for kind in ("package", "service"):
            for name in ("shared-utils", "shared_utils"):
                with self.assertRaisesRegex(ValueError, "already exists"):
                    scaffold.create(kind, name, self.root)
        self.assertEqual(marker.read_text(encoding="utf-8"), "keep me")

    def test_distribution_name_collision_is_rejected(self) -> None:
        existing = self.root / "services" / "different-directory"
        existing.mkdir()
        (existing / "pyproject.toml").write_text(
            '[project]\nname = "Shared.Utils"\n', encoding="utf-8"
        )
        with self.assertRaisesRegex(ValueError, "already exists"):
            scaffold.create("package", "shared-utils", self.root)

    def test_template_failure_leaves_no_partial_project(self) -> None:
        shutil.rmtree(self.root / "templates/service/src/service_name")
        with self.assertRaises(FileNotFoundError):
            scaffold.create("service", "broken", self.root)
        self.assertEqual(list((self.root / "services").iterdir()), [])
        self.assertEqual(
            sorted(path.name for path in self.root.iterdir()), ["packages", "services", "templates"]
        )

    def test_underscore_name_and_cache_exclusion(self) -> None:
        cache = self.root / "templates/package/src/package_name/__pycache__"
        cache.mkdir(exist_ok=True)
        (cache / "stale.pyc").write_bytes(b"cached bytecode")
        project = scaffold.create("package", "shared_utils", self.root)
        self.assertTrue((project / "src/shared_utils/__init__.py").is_file())
        self.assertEqual(list(project.rglob("*.pyc")), [])

    @unittest.skipUnless(shutil.which("make"), "GNU Make is optional")
    def test_make_passes_invalid_name_as_one_argument(self) -> None:
        shutil.copy2(ROOT / "Makefile", self.root / "Makefile")
        shutil.copytree(
            ROOT / "scripts", self.root / "scripts", ignore=shutil.ignore_patterns("__pycache__")
        )
        result = subprocess.run(
            ["make", "new-package", 'name=bad"; touch unexpected; #'],
            cwd=self.root,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((self.root / "unexpected").exists())
        self.assertEqual(list((self.root / "packages").iterdir()), [])

    def test_cli_works_outside_repository(self) -> None:
        shutil.copytree(
            ROOT / "scripts", self.root / "scripts", ignore=shutil.ignore_patterns("__pycache__")
        )
        result = subprocess.run(
            [sys.executable, str(self.root / "scripts/scaffold.py"), "package", "cli-project"],
            cwd=self.root.parent,
            capture_output=True,
            text=True,
            check=True,
        )
        self.assertIn("packages/cli-project", result.stdout.replace("\\", "/"))
        self.assertTrue((self.root / "packages/cli-project/pyproject.toml").is_file())


if __name__ == "__main__":
    unittest.main()
