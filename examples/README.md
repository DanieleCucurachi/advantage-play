# Examples

- `notebooks/higher_lower_strategies.ipynb` — solo and 5-player experiments comparing the five
  Higher-Lower strategies, with paired gaps to trivial and to the optimal baseline, win rates, a
  seat-order effect and hit rate by card on the table. Runs in about 30 seconds.

Install the notebook tooling with `uv sync --group notebooks`, then `uv run jupyter lab`.
Notebook outputs are stripped on commit by `nbstripout` (via pre-commit) to keep diffs reviewable;
commit rendered results to `docs/` instead if they should be kept.
