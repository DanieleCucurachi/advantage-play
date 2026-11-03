"""Shared pytest fixtures."""

import numpy as np
import pytest

SEED = 20240601


@pytest.fixture
def rng() -> np.random.Generator:
    """Deterministic random generator so statistical tests are reproducible."""
    return np.random.default_rng(SEED)
