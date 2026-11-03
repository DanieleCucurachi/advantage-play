"""End-to-end checks of the simulation runner."""

from typing import TYPE_CHECKING

import numpy as np
import pytest

from advantage_play.analysis import mean_ci
from advantage_play.games import HigherLower
from advantage_play.simulation import simulate
from advantage_play.strategies.higher_lower import (
    CardCounting,
    CountingAdvanced,
    OptimalCounting,
    RandomGuess,
    Trivial,
)

if TYPE_CHECKING:
    from advantage_play.games.higher_lower import Guess, Observation
    from advantage_play.strategies import Strategy


def test_same_seed_gives_the_same_scores_whatever_the_number_of_games() -> None:
    players: list[Strategy[Observation, Guess]] = [Trivial(), RandomGuess()]
    short = simulate(HigherLower(), players, n_games=10, seed=1)
    long = simulate(HigherLower(), players, n_games=20, seed=1)

    assert short.shape == (10, 2)
    np.testing.assert_array_equal(short, long[:10])


@pytest.mark.statistical
def test_a_solo_random_player_scores_27_on_average() -> None:
    # Each of the 51 guesses is right with probability 1/2 + 1/2 * P(tie) = 1/2 + 1/2 * 3/51,
    # so the expected score is exactly 51 * (1/2 + 3/102) = 27.
    scores = simulate(HigherLower(), [RandomGuess()], n_games=5000, seed=0)
    mean, half_width = mean_ci(scores, confidence=0.9999)

    assert abs(mean[0] - 27) < half_width[0]


@pytest.mark.statistical
def test_optimal_counting_beats_every_other_strategy_solo() -> None:
    # Same deals for everyone, so the paired difference is tight even with few games.
    optimal = simulate(HigherLower(), [OptimalCounting()], n_games=3000, seed=0)
    others: dict[str, Strategy[Observation, Guess]] = {
        "random": RandomGuess(),
        "trivial": Trivial(),
        "counting": CardCounting(),
        "counting advanced": CountingAdvanced(),
    }
    for name, strategy in others.items():
        mean, half_width = mean_ci(optimal - simulate(HigherLower(), [strategy], 3000, seed=0))
        assert mean[0] - half_width[0] > 0, name
