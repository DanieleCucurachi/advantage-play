"""Decision rules of the Higher-Lower strategies."""

import numpy as np
import pytest

from advantage_play.cards import Card
from advantage_play.games.higher_lower import Guess, Observation
from advantage_play.strategies import Strategy
from advantage_play.strategies.higher_lower import (
    CardCounting,
    CountingAdvanced,
    OptimalCounting,
    RandomGuess,
    Trivial,
)

HIGHER, LOWER = Guess.HIGHER, Guess.LOWER


def observe(*ranks: int) -> Observation:
    """Observation after these ranks were revealed; the last one is on the table."""
    return Observation([Card(rank, "♠") for rank in ranks])


def guesses(
    strategy: Strategy[Observation, Guess], observation: Observation, n: int = 1000
) -> set[Guess]:
    rng = np.random.default_rng(0)
    return {strategy.act(observation, rng) for _ in range(n)}


@pytest.mark.parametrize(("rank", "expected"), [(1, HIGHER), (6, HIGHER), (8, LOWER), (13, LOWER)])
def test_trivial_bets_on_the_larger_side(rank: int, expected: Guess) -> None:
    assert Trivial().act(observe(rank), np.random.default_rng(0)) == expected


def test_trivial_flips_a_coin_on_seven() -> None:
    assert guesses(Trivial(), observe(7)) == {HIGHER, LOWER}


def test_random_guesses_both_ways_about_equally() -> None:
    rng = np.random.default_rng(0)
    n_higher = sum(RandomGuess().act(observe(7), rng) is HIGHER for _ in range(1000))

    assert 430 < n_higher < 570


@pytest.mark.parametrize(
    ("seen", "expected"),
    [
        ((13, 12, 1), HIGHER),  # extreme table cards ignore the count...
        ((1, 2, 3, 13), LOWER),  # ...even when it points the other way
        ((1, 2, 5), HIGHER),  # middle card, more low than high cards gone: high cards remain
        ((13, 12, 5), LOWER),  # middle card, more high than low cards gone
        ((1, 13, 9), LOWER),  # equal counts default to lower
    ],
)
def test_card_counting(seen: tuple[int, ...], expected: Guess) -> None:
    assert CardCounting().act(observe(*seen), np.random.default_rng(0)) == expected


@pytest.mark.parametrize(
    ("seen", "expected"),
    [
        ((13, 12, 11, 4), HIGHER),  # A-4 on the table: always higher, even if the count says lower
        ((1, 1, 1, 10), LOWER),  # 10-K on the table: always lower, even if the count says higher
        ((12, 7), LOWER),  # 7: more highs than lows gone -> lower
        ((1, 7), HIGHER),  # 7: more lows than highs gone -> higher
        ((7, 6), HIGHER),  # 6, delta 0: trivial strategy
        ((10, 10, 11, 11, 12, 12, 6), HIGHER),  # 6 (distance 1), delta 6: 1 > (8 - 6) / 2 is false
        ((10, 10, 11, 11, 12, 12, 13, 6), LOWER),  # 6, delta 7: 1 > (8 - 7) / 2
        ((10, 11, 12, 13, 5), HIGHER),  # 5 (distance 2), delta 4: 2 > (8 - 4) / 2 is false
        ((10, 11, 12, 13, 10, 5), LOWER),  # 5, delta 5: 2 > (8 - 5) / 2
        ((9, 8), LOWER),  # 8, delta 0: trivial strategy
        ((1, 1, 2, 2, 3, 3, 8), LOWER),  # 8 (distance 1), delta -6: 1 > (8 - 6) / 2 is false
        ((1, 1, 2, 2, 3, 3, 4, 8), HIGHER),  # 8, delta -7: 1 > (8 - 7) / 2
        ((1, 2, 3, 4, 9), LOWER),  # 9 (distance 2), delta -4: 2 > (8 - 4) / 2 is false
        ((1, 2, 3, 4, 1, 9), HIGHER),  # 9, delta -5: 2 > (8 - 5) / 2
    ],
)
def test_counting_advanced(seen: tuple[int, ...], expected: Guess) -> None:
    assert CountingAdvanced().act(observe(*seen), np.random.default_rng(0)) == expected


def test_counting_advanced_flips_a_coin_on_a_seven_with_balanced_counts() -> None:
    assert guesses(CountingAdvanced(), observe(1, 13, 7)) == {HIGHER, LOWER}


@pytest.mark.parametrize(
    ("seen", "expected"),
    [
        ((8,), LOWER),  # nothing else seen: the basic rule (28 lower cards left vs 20 higher)
        ((6,), HIGHER),
        (
            (
                7,
                7,
                7,
                7,
                8,
                8,
                8,
                8,
                9,
                9,
                9,
                9,
                10,
                10,
                10,
                10,
                11,
                11,
                11,
                11,
                12,
                12,
                12,
                12,
                13,
                13,
                13,
                13,
                6,
            ),
            LOWER,
        ),  # every card above the 6 is gone: only lower ones are left
        (
            (1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 7, 8),
            HIGHER,
        ),  # every card below the 8 is gone: only higher ones are left
    ],
)
def test_optimal_counting_bets_on_the_side_with_more_cards_left(
    seen: tuple[int, ...], expected: Guess
) -> None:
    assert OptimalCounting().act(observe(*seen), np.random.default_rng(0)) == expected


@pytest.mark.parametrize("seen", [(7,), (1, 1, 1, 1, 2, 2, 2, 2, 8)])
def test_optimal_counting_flips_a_coin_when_both_sides_are_equally_likely(
    seen: tuple[int, ...],
) -> None:
    # A fresh 7 has 24 cards on each side; after eight low cards, an 8 has 20 on each side.
    assert guesses(OptimalCounting(), observe(*seen)) == {HIGHER, LOWER}
