"""Summary statistics for simulated scores (rows are independent games, columns are players)."""

from collections.abc import Sequence

import numpy as np
import pandas as pd
from numpy.typing import NDArray
from scipy import stats


def mean_ci(
    x: NDArray[np.float64], confidence: float = 0.95
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Mean and confidence-interval half-width of each column of ``x``."""
    n = len(x)
    mean: NDArray[np.float64] = x.mean(axis=0)
    half_width: NDArray[np.float64] = (
        stats.t.ppf((1 + confidence) / 2, n - 1) * x.std(axis=0, ddof=1) / np.sqrt(n)
    )
    return mean, half_width


def win_shares(scores: NDArray[np.float64]) -> NDArray[np.float64]:
    """Each game's win, split evenly between the players tied for the top score."""
    best = scores == scores.max(axis=1, keepdims=True)
    shares: NDArray[np.float64] = best / best.sum(axis=1, keepdims=True)
    return shares


def summarize(
    scores: NDArray[np.float64], labels: Sequence[str], confidence: float = 0.95
) -> pd.DataFrame:
    """Per-player mean score and win rate, each with a confidence-interval half-width."""
    score, score_ci = mean_ci(scores, confidence)
    win_rate, win_rate_ci = mean_ci(win_shares(scores), confidence)
    return pd.DataFrame(
        {"score": score, "score_ci": score_ci, "win_rate": win_rate, "win_rate_ci": win_rate_ci},
        index=pd.Index(labels, name="player"),
    )


def paired_difference(
    scores: NDArray[np.float64], labels: Sequence[str], confidence: float = 0.95
) -> pd.DataFrame:
    """Mean score of every other player minus the first one's, paired game by game.

    Pairing removes the luck of the deal, so differences are far tighter than comparing the
    confidence intervals of ``summarize``. For two separate runs, call ``mean_ci(a - b)``
    on their scores (same seed and number of games).
    """
    diff, diff_ci = mean_ci(scores[:, 1:] - scores[:, [0]], confidence)
    return pd.DataFrame(
        {"score_diff": diff, "score_diff_ci": diff_ci}, index=pd.Index(labels[1:], name="player")
    )
