# Hydra configuration

One directory per **config group**; each YAML file is one selectable option.

| Group       | Purpose                                                          | Options                                      |
| ----------- | ---------------------------------------------------------------- | -------------------------------------------- |
| `game/`     | The game and its rules                                           | `higher_lower`                               |
| `strategy/` | One file per strategy                                            | `random`, `trivial`, `counting`, `counting_advanced`, `optimal_counting` |
| `players/`  | Who sits at the table: strategies, labelled and in seat order    | `head_to_head` (all 5 strategies), `solo_<strategy>` for each strategy |

Plain values live in `config.yaml`: `n_games`, `confidence`, `seed`.

Every config uses `_target_` with `hydra.utils.instantiate`, so games and strategies are built
straight from config, without a registry. Rule variants are config values, so a new variant is a
new YAML file, not new code.

A `players/` file lists strategies from `strategy/` under the label they get in the results:

```yaml
# @package players
defaults:
  - /strategy@hero: counting
  - /strategy@rival_1: random
  - /strategy@rival_2: random
```

Every file in `players/` is run by the test suite, so a broken line-up fails CI.
