# advantage-play

A framework for finding optimal play in card games. Define **any** card game from a set of rules,
plug in a **strategy**, run **reproducible Monte Carlo simulations** and get **statistically sound
results** — expected value, house edge, variance, risk of ruin — with confidence intervals and plots.

> **Status:** project scaffold. Tooling, CI and the package layout are in place; the game, strategy
> and simulation code is yet to be written. See the [roadmap](#roadmap).

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

## Planned usage

```bash
# one experiment
uv run python -m advantage_play game=blackjack strategy=basic simulation.n_episodes=1_000_000

# compare strategies across rule variants (Hydra multirun)
uv run python -m advantage_play -m game=blackjack,blackjack_h17 strategy=basic,hi_lo,random
```

Each run writes its resolved config, raw results and report to `outputs/<date>/<time>/`.

## Repository layout

```
├── src/advantage_play/   # the package (src layout)
│   ├── cards/            #   cards, decks, shoes, shuffling
│   ├── games/            #   rules, state, legal actions, payoffs
│   ├── strategies/       #   decision policies
│   ├── simulation/       #   seeded, parallel Monte Carlo engine
│   └── analysis/         #   statistics, CIs, plots, reports
├── conf/                 # Hydra config groups: game/ strategy/ simulation/ analysis/
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

## Roadmap

1. Cards: `Card`, `Deck`/`Shoe`, seeded shuffling.
2. Game and strategy interfaces; Blackjack with configurable rules; basic strategy.
3. Simulation runner with deterministic parallel seeding; Hydra entry point.
4. Analysis: EV/house edge with CIs, strategy comparison, plots, run reports.
5. More games, card counting, strategy optimisation (e.g. exhaustive/DP, RL).

## License

Apache-2.0 — see [LICENSE](LICENSE).
