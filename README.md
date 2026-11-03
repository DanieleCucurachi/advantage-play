# advantage-play

A framework for finding optimal play in card games. Define **any** card game from a set of rules,
plug in a **strategy**, run **reproducible Monte Carlo simulations** and get **statistically sound
results** — expected value, house edge, variance, risk of ruin — with confidence intervals and plots.

> **Status:** early. The framework core and the first game (Higher-Lower, with five strategies
> including an optimal baseline) are implemented. See the [roadmap](#roadmap).

## Design goals

- **General** — Blackjack first, but nothing is Blackjack-specific: any game played with standard
  52-card decks (one or many) should be expressible.
- **Config-driven** — games, rule variants, strategies and experiments are composed with
  [Hydra](https://hydra.cc); a new rule variant is a YAML file, and sweeps are one flag away.
- **Reproducible** — one master seed; independent random streams per worker.
- **Statistically honest** — every estimate comes with a confidence interval and sample size.
- **Typed and tested** — strict `mypy`, `ruff`, `pytest` + `hypothesis`, enforced in CI.

See [docs/architecture.md](docs/architecture.md) for the planned design.

## Quickstart

Requires [uv](https://docs.astral.sh/uv/getting-started/installation/).

```bash
git clone <repo-url> && cd advantage-play
make install        # uv sync: creates .venv with the pinned Python and all dev dependencies
make hooks          # optional: install pre-commit / pre-push git hooks
make check          # lint + types + fast tests
```

Common tasks (`make help` lists all):

| Command          | What it does                                   |
| ---------------- | ---------------------------------------------- |
| `make test`      | Full test suite (parallel)                     |
| `make cov`       | Tests with coverage report                     |
| `make format`    | Auto-fix lint issues and format                |
| `make notebooks` | Install Jupyter tooling (`uv sync --group notebooks`) |
| `make docs`      | Build the HTML docs to `docs/_build/html`      |
| `make docs-live` | Serve the docs locally with auto-reload        |

Dependencies are managed with uv: `uv add <pkg>`, `uv add --group dev <pkg>`, then commit `uv.lock`.

## Usage

```bash
# all 5 strategies at one table (the default experiment)
uv run python -m advantage_play

# a strategy alone through the deck: its raw hit rate
uv run python -m advantage_play players=solo_counting n_games=100000

# compare strategies solo on identical deals (Hydra multirun, same seed => paired)
uv run python -m advantage_play -m players=solo_random,solo_trivial,solo_counting
```

Each run logs the mean score and win rate per player with confidence intervals, plus paired score
differences against the first player, and saves `scores.csv`, `summary.csv` and the resolved
config to `outputs/<date>/<time>/`. Add a game, strategy or line-up by adding a YAML file in
`conf/` (see [conf/README.md](conf/README.md)).

Higher-Lower strategies (`strategies/higher_lower.py`, one config per strategy in `conf/strategy/`):

| Strategy | Idea |
| --- | --- |
| `random` | Guess higher or lower with equal probability. |
| `trivial` | Lower above 7, higher below 7, coin flip on 7. |
| `counting` | Trivial on A-4 and 10-K; on 5-9 follow the count of low vs high cards seen. |
| `counting_advanced` | Trivial on A-4 and 10-K, count on the 7; on 5, 6, 8, 9 the delta count (10-K minus A-4 seen) decides when to go against the card's own side. |
| `optimal_counting` | Bet on the side with more cards left in the deck. |

Notes on interpreting results:

- **Ground truth.** `optimal_counting` maximises every single guess, so solo it gives the best
  possible expected score and no strategy can beat it. At a table with opponents a guess also
  decides who plays next, so it is not guaranteed to maximise the win rate.

- **Solo vs. multi-player.** In multi-player games the cyclic seat order matters: a player
  inherits the card that beat the previous player, so who sits before whom shifts the scores. Use
  solo runs for a clean strategy comparison and multi-player runs for win rates.
- **Worked example.** [examples/notebooks/higher_lower_strategies.ipynb](examples/notebooks/higher_lower_strategies.ipynb)
  runs both experiments for all five strategies and plots the results.
- **Paired comparisons.** Runs with the same `seed` and `n_games` play identical deals, so
  `analysis.mean_ci(a - b)` on two runs' `scores.csv` gives a far tighter difference than
  comparing the two confidence intervals.

## Repository layout

```
├── src/advantage_play/   # the package (src layout)
│   ├── cards/            #   cards, decks, shoes, shuffling
│   ├── games/            #   rules, state, legal actions, payoffs
│   ├── strategies/       #   decision policies
│   ├── simulation/       #   seeded, parallel Monte Carlo engine
│   └── analysis/         #   statistics, CIs, plots, reports
├── conf/                 # Hydra config groups: game/ strategy/ players/
├── tests/                # unit/ and integration/ tests, data/ for small fixtures
├── examples/notebooks/   # exploratory notebooks
├── docs/                 # Sphinx docs (Furo + MyST); API reference is auto-generated from docstrings
├── .github/              # CI, release workflow, Dependabot, issue/PR templates
└── pyproject.toml        # metadata, dependency groups, tool config (ruff, mypy, pytest, coverage)
```

## CI/CD

- **CI** ([ci.yml](.github/workflows/ci.yml)) on every PR and push to `main`: lockfile check, ruff,
  mypy (strict), pytest on Python 3.11–3.13 (+ macOS) with coverage, package build + wheel smoke
  test. Require the single **CI ok** check in branch protection.
- **Docs** ([docs.yml](.github/workflows/docs.yml)): CI builds the Sphinx docs with warnings as
  errors; pushes to `main` publish them to GitHub Pages (Settings → Pages → Source: GitHub Actions).
- **Release** ([release.yml](.github/workflows/release.yml)): push a tag `vX.Y.Z` matching
  `pyproject.toml` → re-runs CI → builds → creates a GitHub release. PyPI publishing (trusted
  publishing) is opt-in via the `PUBLISH_TO_PYPI` repository variable.
- **Dependabot** keeps Python dependencies and GitHub Actions current.

## License

Apache-2.0 — see [LICENSE](LICENSE).
