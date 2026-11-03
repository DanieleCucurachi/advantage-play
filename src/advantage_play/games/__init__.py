"""Game definitions: state, legal actions, transitions and payoffs, driven by config."""

from advantage_play.games.base import Game
from advantage_play.games.higher_lower import HigherLower

__all__ = ["Game", "HigherLower"]
