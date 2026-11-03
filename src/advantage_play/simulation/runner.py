"""Seeded Monte Carlo runner."""

from collections.abc import Sequence

import numpy as np
from numpy.typing import NDArray

from advantage_play.games.base import Act, Game, Obs
from advantage_play.strategies.base import Strategy


def simulate(
    game: Game[Obs, Act],
    strategies: Sequence[Strategy[Obs, Act]],
    n_games: int,
    seed: int,
) -> NDArray[np.float64]:
    """Play ``n_games`` games and return the scores, shape ``(n_games, n_players)``.

    Game ``i`` always gets the same random stream for a given ``seed`` (``SeedSequence.spawn``).
    Results therefore do not depend on how games are batched, and line-ups of the same size see
    identical deals, so strategies can be compared game by game (paired).
    """
    streams = np.random.SeedSequence(seed).spawn(n_games)
    return np.array(
        [game.play(strategies, np.random.default_rng(stream)) for stream in streams], dtype=float
    )
