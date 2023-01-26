import ast
from typing import Set

from flake8_no_debug_vars import Plugin


def _results(s: str) -> Set[str]:
    tree = ast.parse(s)
    plugin = Plugin(tree)
    return {f"{line}: {col} {msg}" for line, col, msg, _ in plugin.run()}


def test_trivial_case():
    assert _results("") == set()


def test_error_cases():
    assert _results("test = True") == set({"1: 0 NDV100 variable 'test' must be false"})
    assert _results("debug = True") == set(
        {"1: 0 NDV100 variable 'debug' must be false"}
    )
    assert _results("TEST = True") == set({"1: 0 NDV100 variable 'TEST' must be false"})
    assert _results("DEBUG = True") == set(
        {"1: 0 NDV100 variable 'DEBUG' must be false"}
    )
    assert _results("test = 1") == set({"1: 0 NDV100 variable 'test' must be false"})
    assert _results("debug = 1") == set({"1: 0 NDV100 variable 'debug' must be false"})
    assert _results("TEST = 1") == set({"1: 0 NDV100 variable 'TEST' must be false"})
    assert _results("DEBUG = 1") == set({"1: 0 NDV100 variable 'DEBUG' must be false"})
    assert _results("def test(): DEBUG = 1") == set(
        {"1: 12 NDV100 variable 'DEBUG' must be false"}
    )
    assert _results("class test():\n    def test(self): DEBUG = 1") == set(
        {"2: 20 NDV100 variable 'DEBUG' must be false"}
    )
    assert _results("class test():\n    def test(self): self.DEBUG = 1") == set(
        {"2: 20 NDV100 variable 'DEBUG' must be false"}
    )


def test_ok_cases():
    assert _results("test = False") == set()
    assert _results("debug = False") == set()
    assert _results("TEST = False") == set()
    assert _results("DEBUG = False") == set()
    assert _results("test = 0") == set()
    assert _results("debug = 0") == set()
    assert _results("TEST = 0") == set()
    assert _results("DEBUG = 0") == set()
    assert _results("def test(): DEBUG = 0") == set()
    assert _results("class test():\n    def test(self): DEBUG = 0") == set()
