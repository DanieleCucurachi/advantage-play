"""Strategies: map the observable game state to an action (fixed tables, counting, learned).

Strategies are game-specific and live next to the game name, e.g. ``strategies.higher_lower``.
"""

from advantage_play.strategies.base import Strategy

__all__ = ["Strategy"]
