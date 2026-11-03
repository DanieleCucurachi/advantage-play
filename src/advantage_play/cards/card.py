"""A standard 52-card deck."""

from typing import NamedTuple

import numpy as np

SUITS = ("♠", "♥", "♦", "♣")


class Card(NamedTuple):
    """A playing card. ``rank`` runs from 1 (Ace) to 13 (King); Jack, Queen, King are 11, 12, 13."""

    rank: int
    suit: str


STANDARD_DECK: tuple[Card, ...] = tuple(Card(rank, suit) for suit in SUITS for rank in range(1, 14))


def shuffled_deck(rng: np.random.Generator) -> list[Card]:
    """Return a freshly shuffled standard deck."""
    deck = list(STANDARD_DECK)
    rng.shuffle(deck)
    return deck
