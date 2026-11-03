# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project adheres to
[Semantic Versioning](https://semver.org/).

## [Unreleased]

### Changed

- The default `head_to_head` line-up now seats all five Higher-Lower strategies.

### Added

- Higher-Lower game with random, trivial and card-counting strategies, a seeded simulation
  runner, summary statistics (confidence intervals, split-win rates, paired differences) and a
  Hydra CLI (`python -m advantage_play`).
- `CountingAdvanced` and `OptimalCounting` strategies for Higher-Lower. The latter bets on the side
  with more cards left in the deck and is the ground truth the others are measured against.
- Notebook comparing all five strategies solo and in 5-player games (averaged over all circular
  seatings): mean score, win rate, paired gaps to trivial and to optimal, seat-order effect and
  hit rate by card on the table.
- Project scaffold: `src/` layout, uv + dependency groups, Hydra config tree, ruff/mypy/pytest
  configuration, pre-commit hooks, GitHub Actions CI and release workflows.
