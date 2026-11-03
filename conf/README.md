# Hydra configuration

One directory per **config group**; each YAML file is one selectable option.

| Group         | Purpose                                                         | Example options          |
| ------------- | --------------------------------------------------------------- | ------------------------ |
| `game/`       | Game rules (decks, payouts, legal actions, termination)         | `blackjack`, `baccarat`  |
| `strategy/`   | Player strategy and its parameters                              | `basic`, `hi_lo`, `random` |
| `simulation/` | Episodes, workers, batching, stopping criteria                  | `default`, `quick`       |
| `analysis/`   | Statistics and reporting (CI level, plots, output formats)      | `default`                |

Use `_target_` with `hydra.utils.instantiate` so games and strategies are built straight from config
without a registry. Rule variants (e.g. dealer hits soft 17, number of decks) are plain config
values, so a new variant is a new YAML file, not new code.
