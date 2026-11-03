"""Interface shared by all card games."""

from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import Generic, TypeVar

import numpy as np

from advantage_play.strategies.base import Strategy

Obs = TypeVar("Obs")
Act = TypeVar("Act")


class Game(ABC, Generic[Obs, Act]):
    """A card game that plays one full game given one strategy per player."""

    @abstractmethod
    def play(
        self, strategies: Sequence[Strategy[Obs, Act]], rng: np.random.Generator
    ) -> tuple[float, ...]:
        """Play one game and return each player's final score, in seat order.

        All setup randomness (shuffle, starting player) must be drawn from ``rng`` before the first
        strategy is called. The same seed then always yields the same deal whatever the strategies
        do, which is what allows paired comparisons between strategies.
        """
