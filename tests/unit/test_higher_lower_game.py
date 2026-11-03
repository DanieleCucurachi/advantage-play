"""Rules of Higher-Lower, checked on scripted decks."""

import numpy as np
import pytest

from advantage_play.cards import Card
from advantage_play.games import HigherLower
from advantage_play.games.higher_lower import Guess, Observation

RNG = np.random.default_rng(0)


class Always:
    """Test strategy that always makes the same guess."""

    def __init__(self, guess: Guess) -> None:
        self.guess = guess

    def act(self, observation: Observation, rng: np.random.Generator) -> Guess:
        return self.guess


def deck(*ranks: int) -> list[Card]:
    return [Card(rank, "♠") for rank in ranks]


def test_correct_guesses_score_and_keep_the_turn() -> None:
    # 1->2 and 2->3 are higher; 3->3 is a tie (always a win); 3->2 is a miss.
    scores = HigherLower().play_deck(deck(1, 2, 3, 3, 2), 0, [Always(Guess.HIGHER)], RNG)

    assert scores == (3,)


def test_a_miss_passes_the_turn_to_the_next_player() -> None:
    # A misses (5->3), so B guesses against the 3: 3->9 and 9->9 (tie) are right, 9->1 is a miss.
    players = [Always(Guess.HIGHER), Always(Guess.HIGHER)]
    scores = HigherLower().play_deck(deck(5, 3, 9, 9, 1), 0, players, RNG)

    assert scores == (0, 2)


@pytest.mark.parametrize(("first_player", "expected"), [(0, (1, 0)), (1, (0, 1))])
def test_the_first_player_makes_the_first_guess(
    first_player: int, expected: tuple[int, int]
) -> None:
    players = [Always(Guess.HIGHER), Always(Guess.HIGHER)]

    assert HigherLower().play_deck(deck(3, 5), first_player, players, RNG) == expected


def test_a_full_game_awards_at_most_one_point_per_guess() -> None:
    players = [Always(Guess.HIGHER), Always(Guess.LOWER), Always(Guess.HIGHER)]
    scores = HigherLower().play(players, np.random.default_rng(0))

    n_guesses = 51  # 52 cards; the last card on the table is never guessed against
    assert len(scores) == 3
    assert 0 <= sum(scores) <= n_guesses
