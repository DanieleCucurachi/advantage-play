# Advantage Play

A research workspace for exploring strategies in games using standard 52-card
decks. Blackjack is one possible future target, not a constraint on the design.

**Status: repository template only.** No card model, game engine, strategy,
simulation runner, statistics implementation, or CLI is implemented yet.

## Getting started

Install [uv](https://docs.astral.sh/uv/getting-started/installation/), then run
these commands from the repository root:

```sh
uv python install
uv sync --locked
```

Python 3.12 is the development baseline, recorded in `.python-version`.
`uv sync` creates `.venv` and installs the package and development tools.
Commit `uv.lock` changes when intentionally updating dependencies with `uv add`
or `uv lock --upgrade`; use `--locked` for reproducible checks.

## Layout

```text
configs/
  config.yaml           # Hydra defaults and output-directory policy
  game/template.yaml    # Standard deck definition and arbitrary game rules
  strategy/template.yaml
  simulation/default.yaml
  reporting/default.yaml
  experiment/smoke.yaml # Small-run configuration preset
src/advantage_play/     # Empty, typed Python package; no application logic
tests/                 # Configuration-template checks
```

The package uses a `src` layout and Hatchling builds. Configurations live at the
repository root for research use; they are included in source distributions but
not installed in the wheel.

## Experiment configuration

[Hydra](https://hydra.cc/docs/intro/) composes independent configuration groups.
Add game and strategy YAML files alongside the templates and select them with
`game=<name>` and `strategy=<name>`. Keep game-specific rules in `game.rules` and
strategy-specific settings in `strategy.parameters`, rather than assuming
blackjack scoring or actions in shared configuration.

The template's game and strategy names are mandatory (`???`). Empty rule,
parameter, and metric collections are placeholders, not complete specifications.
YAML configuration does not enforce legal rules, parameter ranges, or implement
the selected algorithms.

You can inspect the configuration now, **without running a simulation**:

```sh
uv run --locked python -c 'from hydra import compose, initialize; from omegaconf import OmegaConf; initialize(config_path="configs", version_base="1.3"); print(OmegaConf.to_yaml(compose(config_name="config", overrides=["experiment=smoke"])))'
```

The smoke preset overrides simulation sizes at the global config level.
Hydra overrides such as `simulation.seed=7` take precedence over presets;
use `+game.rules.<key>=<value>` to add a new rule to the empty mapping.
Future runners should reject missing settings before executing.

The output policy reserves timestamped `outputs/` directories for single runs
and numbered subdirectories under `multirun/` for sweeps, without changing the
working directory. These directories are ignored by Git. The Compose API preview
above does not launch Hydra jobs, create run directories, or save run metadata.
A future Hydra entry point will be needed for `--multirun` execution and automatic
`.hydra/` configuration snapshots.

## Development

```sh
uv run --locked ruff check .
uv run --locked ruff format --check .
uv run --locked pytest
uv build
```

CI runs the same checks. Tests currently validate only configuration composition,
mandatory placeholders, overrides, and output settings—not game correctness.

## Implementation direction

Keep future components separate: card/deck primitives, rule-driven game state
and legal actions, strategies that consume only permitted observations,
simulation orchestration, and statistical reporting. Add dependencies for
numerics, plots, or notebooks when those implementations need them.

For reproducible experiments, record the seed, resolved configuration, code
revision, and dependency lockfile. Define how repetitions receive independent
random streams; setting a seed in YAML alone does not seed an RNG.
Reports should eventually include sample sizes, outcome distributions, uncertainty
intervals with documented assumptions, and comparisons against baselines—not just
average returns. These are design goals, not existing capabilities.

## License

Apache-2.0; see [LICENSE](LICENSE).