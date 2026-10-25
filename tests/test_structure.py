# Checks the base project layout (T02, plan section 1).
import importlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def test_t02_package_imports():
    module = importlib.import_module("pelis_cat")
    assert module is not None


def test_t02_base_folders_exist():
    for name in ["pelis_cat", "tests", "templates", "data"]:
        assert (ROOT / name).is_dir(), f"missing folder: {name}"
