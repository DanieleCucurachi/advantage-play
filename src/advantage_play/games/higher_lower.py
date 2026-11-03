"""Higher-Lower: guess whether the next card is higher or lower than the one on the table."""

from collections.abc import Sequence
from dataclasses import dataclass
from enum import Enum, auto

import numpy as np

from advantage_play.cards import Card, shuffled_deck
from advantage_play.games.base import Game
from advantage_play.strategies.base import Strategy


class Guess(Enum):
    """The two possible actions."""

    HIGHER = auto()
    LOWER = auto()


@dataclass(frozen=True, slots=True)
class Observation:
    """What a player sees: every card revealed so far, the last one being on the table."""

    seen: Sequence[Card]

    @property
    def table_card(self) -> Card:
        """The card the next one is compared against."""
        return self.seen[-1]


def _is_correct(guess: Guess, table: Card, drawn: Card) -> bool:
    """Ties count as correct whatever the guess."""
    if drawn.rank == table.rank:
        return True
    return (drawn.rank > table.rank) == (guess is Guess.HIGHER)


class HigherLower(Game[Observation, Guess]):
    """One 52-card deck, players take turns in a circle starting from a random one.

    The player to move guesses whether the next card is higher or lower than the one on the table,
    and scores one point per correct guess. A miss passes the turn to the next player, who guesses
    against the card that just beat the previous one. The game ends when the deck runs out; the last
    card on the table scores for nobody. Ranks are Ace=1, ..., King=13. A single player is allowed
    (solo analysis of a strategy): a miss then simply gives the turn back to them.
    """

    def play(
        self, strategies: Sequence[Strategy[Observation, Guess]], rng: np.random.Generator
    ) -> tuple[float, ...]:
        """Shuffle, pick the first player at random and play the deck through."""
        if not strategies:
            raise ValueError("at least one player is required")
        deck = shuffled_deck(rng)
        first_player = int(rng.integers(len(strategies)))
        return self.play_deck(deck, first_player, strategies, rng)

    def play_deck(
        self,
        deck: Sequence[Card],
        first_player: int,
        strategies: Sequence[Strategy[Observation, Guess]],
        rng: np.random.Generator,
    ) -> tuple[float, ...]:
        """Play a given (already shuffled) deck; ``deck[0]`` is the first card on the table."""
        scores = [0] * len(strategies)
        player = first_player
        for i in range(1, len(deck)):
            guess = strategies[player].act(Observation(deck[:i]), rng)
            if _is_correct(guess, table=deck[i - 1], drawn=deck[i]):
                scores[player] += 1
            else:
                player = (player + 1) % len(strategies)
        return tuple(scores)
