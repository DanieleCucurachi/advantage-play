"""Tests for the summary statistics."""

import numpy as np
import pytest

from advantage_play.analysis import mean_ci, paired_difference, summarize, win_shares


def test_mean_ci_matches_the_textbook_t_interval() -> None:
    mean, half_width = mean_ci(np.array([[1.0], [2.0], [3.0], [4.0], [5.0]]))

    # t(0.975, df=4) * s / sqrt(n) = 2.7764 * 1.5811 / 2.2361
    assert mean == pytest.approx([3.0])
    assert half_width == pytest.approx([1.9632], rel=1e-4)


def test_win_shares_split_ties_and_sum_to_one() -> None:
    shares = win_shares(np.array([[3.0, 3.0, 1.0], [0.0, 5.0, 2.0]]))

    assert shares.tolist() == [[0.5, 0.5, 0.0], [0.0, 1.0, 0.0]]


def test_summarize_reports_score_and_win_rate_per_player() -> None:
    summary = summarize(np.array([[3.0, 1.0], [2.0, 2.0], [1.0, 3.0]]), ["a", "b"])

    assert summary.index.tolist() == ["a", "b"]
    assert summary["score"].tolist() == [2.0, 2.0]
    assert summary["win_rate"].tolist() == [0.5, 0.5]


def test_paired_difference_cancels_the_luck_of_the_deal() -> None:
    # Scores swing wildly from game to game, but b is always exactly 2 above a.
    scores = np.array([[1.0, 3.0], [10.0, 12.0], [5.0, 7.0]])
    diff = paired_difference(scores, ["a", "b"])

    assert diff.index.tolist() == ["b"]
    assert diff["score_diff"].tolist() == [2.0]
    assert diff["score_diff_ci"].tolist() == [0.0]
