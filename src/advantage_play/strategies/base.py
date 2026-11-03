"""Interface shared by all strategies."""

from typing import Protocol, TypeVar

import numpy as np

Obs_contra = TypeVar("Obs_contra", contravariant=True)
Act_co = TypeVar("Act_co", covariant=True)


class Strategy(Protocol[Obs_contra, Act_co]):
    """Chooses an action from what the player can observe.

    Strategies are stateless: everything they may use (e.g. every card revealed so far) must be
    in the observation. Any randomness must be drawn from the ``rng`` passed in.
    """

    def act(self, observation: Obs_contra, rng: np.random.Generator) -> Act_co:
        """Return the action to play for this observation."""
        ...
