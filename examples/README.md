# Examples

- `notebooks/` — exploratory analysis and worked examples (Jupyter).

Install the notebook tooling with `uv sync --group notebooks`, then `uv run jupyter lab`.
Notebook outputs are stripped on commit by `nbstripout` (via pre-commit) to keep diffs reviewable;
commit rendered results to `docs/` instead if they should be kept.
