"""Tests for the standard deck."""

from collections import Counter

import numpy as np

from advantage_play.cards import STANDARD_DECK, shuffled_deck


def test_standard_deck_has_13_ranks_in_4_suits() -> None:
    assert len(set(STANDARD_DECK)) == 52
    assert Counter(card.rank for card in STANDARD_DECK) == dict.fromkeys(range(1, 14), 4)


def test_shuffled_deck_is_a_reproducible_permutation() -> None:
    deck = shuffled_deck(np.random.default_rng(0))

    assert sorted(deck) == sorted(STANDARD_DECK)
    assert deck != list(STANDARD_DECK)
    assert deck == shuffled_deck(np.random.default_rng(0))
