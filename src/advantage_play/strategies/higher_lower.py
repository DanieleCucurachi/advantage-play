"""Strategies for Higher-Lower."""

from collections import Counter

import numpy as np

from advantage_play.cards import STANDARD_DECK
from advantage_play.games.higher_lower import Guess, Observation

MIDDLE_RANK = 7
LOW_MAX_RANK = 4  # Ace to 4 are "low" cards
HIGH_MIN_RANK = 10  # 10, Jack, Queen, King are "high" cards

_CARDS_PER_RANK = Counter(card.rank for card in STANDARD_DECK)


def _coin_flip(rng: np.random.Generator) -> Guess:
    return Guess.HIGHER if rng.random() < 0.5 else Guess.LOWER


class RandomGuess:
    """Guess higher or lower with equal probability."""

    def act(self, observation: Observation, rng: np.random.Generator) -> Guess:
        """Flip a coin."""
        return _coin_flip(rng)


class Trivial:
    """Bet on the larger side of the table card: lower above 7, higher below 7, coin flip on 7."""

    def act(self, observation: Observation, rng: np.random.Generator) -> Guess:
        """Compare the table card with the middle rank."""
        rank = observation.table_card.rank
        if rank == MIDDLE_RANK:
            return _coin_flip(rng)
        return Guess.LOWER if rank > MIDDLE_RANK else Guess.HIGHER


class CardCounting:
    """Trivial strategy on extreme cards; on middle cards, follow what has left the deck.

    Counts the low (A-4) and high (10-K) cards revealed so far, whoever's turn it was. If more low
    than high cards are gone, the rest of the deck is richer in high cards, so guess higher;
    otherwise guess lower.
    """

    def act(self, observation: Observation, rng: np.random.Generator) -> Guess:
        """Guess from the table card and the low/high count."""
        rank = observation.table_card.rank
        if rank <= LOW_MAX_RANK:
            return Guess.HIGHER
        if rank >= HIGH_MIN_RANK:
            return Guess.LOWER
        n_low = sum(card.rank <= LOW_MAX_RANK for card in observation.seen)
        n_high = sum(card.rank >= HIGH_MIN_RANK for card in observation.seen)
        return Guess.HIGHER if n_low > n_high else Guess.LOWER


class CountingAdvanced:
    """Card counting whose decision on every middle card depends on its distance from the 7.

    Counts the low (A-4) and high (10-K) cards revealed so far; ``delta`` is highs seen minus lows
    seen, so a positive delta means the rest of the deck is poorer in high cards.

    - Table card A-4: higher. Table card 10-K: lower.
    - 7: lower if ``delta > 0``, higher if ``delta < 0``, coin flip if ``delta == 0``.
    - 5-6, at distance ``d`` from the 7: lower if ``d > (8 - delta) / 2``, otherwise higher.
    - 8-9, at distance ``d`` from the 7: higher if ``d > (8 + delta) / 2``, otherwise lower.

    With zero delta this is the trivial strategy. A card goes against its own rank once ``delta``
    passes ``8 - 2d`` towards the other side: 6 and 8 need a delta beyond 6, 5 and 9 beyond 4.
    """

    def act(self, observation: Observation, rng: np.random.Generator) -> Guess:
        """Guess from the table card, its distance from the 7 and the delta count."""
        rank = observation.table_card.rank
        if rank <= LOW_MAX_RANK:
            return Guess.HIGHER
        if rank >= HIGH_MIN_RANK:
            return Guess.LOWER
        delta = sum(card.rank >= HIGH_MIN_RANK for card in observation.seen) - sum(
            card.rank <= LOW_MAX_RANK for card in observation.seen
        )
        distance = abs(rank - MIDDLE_RANK)
        if rank == MIDDLE_RANK:
            return _coin_flip(rng) if delta == 0 else (Guess.LOWER if delta > 0 else Guess.HIGHER)
        if rank < MIDDLE_RANK:
            return Guess.LOWER if distance > (8 - delta) / 2 else Guess.HIGHER
        return Guess.HIGHER if distance > (8 + delta) / 2 else Guess.LOWER


class OptimalCounting:
    """Count every rank, then bet on the side with more cards left in the deck.

    The chance of a correct guess is the cards left on that side plus the cards that tie with the
    table card (a tie wins either way), over the cards left. Ties add equally to both sides, so
    comparing the two sides is enough; equal counts (e.g. a 7 on a fresh deck) get a coin flip.

    This maximises every single guess, which maximises the expected score when playing solo: it is
    the ground truth the other strategies are measured against. At a table with opponents a guess
    also decides who plays next, so it is not guaranteed to maximise the chance of winning.
    """

    def act(self, observation: Observation, rng: np.random.Generator) -> Guess:
        """Guess the side with more cards left."""
        rank = observation.table_card.rank
        left = _CARDS_PER_RANK - Counter(card.rank for card in observation.seen)
        n_higher = sum(n for left_rank, n in left.items() if left_rank > rank)
        n_lower = sum(n for left_rank, n in left.items() if left_rank < rank)
        if n_higher == n_lower:
            return _coin_flip(rng)
        return Guess.HIGHER if n_higher > n_lower else Guess.LOWER
