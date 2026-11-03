# Architecture

## Core abstractions

| Concept      | Where                            | Responsibility                                                              |
| ------------ | -------------------------------- | --------------------------------------------------------------------------- |
| `Card`       | `cards`                          | Rank 1 (Ace) to 13 (King) and suit; `shuffled_deck(rng)` for a 52-card deck |
| `Game`       | `games.base` (ABC)               | `play(strategies, rng)` plays one full game and returns each player's score |
| `Strategy`   | `strategies.base` (Protocol)     | `act(observation, rng)` maps what a player can observe to an action         |
| `simulate`   | `simulation`                     | Plays N seeded games; returns scores of shape `(n_games, n_players)`        |
| statistics   | `analysis`                       | Means, confidence intervals, split-win rates, paired differences            |

A game defines its own `Observation` and action types (e.g. `games.higher_lower`), and its
strategies live next to it (`strategies.higher_lower`). Any object with a matching `act` method is
a strategy; no inheritance is needed. Strategies are stateless: everything they may use, such as
every card revealed so far, is in the observation.

## Data flow

```
Hydra config ──instantiate──► Game + strategies ──► simulate ──► scores (n_games x n_players)
                                                                        │
                                              summarize / paired_difference ◄┘ ──► log + CSVs in outputs/
```

## Principles

- **Reproducibility:** a master seed is split with `SeedSequence.spawn` into one stream per game, so
  results do not depend on batching or, later, on the number of workers.
- **Paired comparisons:** a game draws its setup (shuffle, starting player) from `rng` before any
  strategy acts, so the same seed always yields the same deal. Runs with the same seed and
  line-up size can be compared game by game, which is far more precise than comparing two
  independent confidence intervals.
- **Statistical rigour:** every estimate is reported with a confidence interval and sample size.
- **Rules are config:** variants are values in YAML, not subclasses.
- **Testing:** rules are tested on scripted decks (`HigherLower.play_deck`); statistical tests are
  seeded, tolerance-based and compared with analytic values (e.g. a random solo player scores 27)
  or with a ground truth (`OptimalCounting` must not lose to any other strategy solo).
