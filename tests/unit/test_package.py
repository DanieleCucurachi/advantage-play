"""Smoke tests: the package imports and exposes its subpackages."""

import importlib

import pytest

import advantage_play


def test_version_is_exposed() -> None:
    assert isinstance(advantage_play.__version__, str)
    assert advantage_play.__version__


@pytest.mark.parametrize("name", ["cards", "games", "strategies", "simulation", "analysis"])
def test_subpackages_import(name: str) -> None:
    importlib.import_module(f"advantage_play.{name}")
