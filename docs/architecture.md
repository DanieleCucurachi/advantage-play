# Architecture (planned)

This is the intended design, to be refined as code lands. Nothing here is implemented yet.

## Core abstractions

| Concept      | Responsibility                                                                 |
| ------------ | ------------------------------------------------------------------------------ |
| `Card`/`Shoe`| 52-card model; one or many decks; seeded shuffle; penetration (cut card)       |
| `Game`       | Rules as data: state, legal actions, transitions, payoff. Built from config    |
| `Strategy`   | Maps the player's *observable* state (not hidden cards) to an action           |
| `Simulator`  | Plays N episodes of `Game` with a `Strategy`; deterministic given the seed     |
| `Analysis`   | Turns raw episode records into estimates, CIs, comparisons, plots              |

Keep `Game` and `Strategy` independent: any strategy that speaks the game's observation/action
interface can be evaluated on it, which is what enables comparisons and sweeps.

## Data flow

```
Hydra config ──instantiate──► Game + Strategy ──► Simulator ──► episode records (DataFrame/Parquet)
                                                                       │
                                                      Analysis ◄───────┘──► report + plots in outputs/
```

## Principles

- **Reproducibility:** a master seed is split with `numpy.random.SeedSequence.spawn` into one
  stream per worker/episode batch, so results do not depend on the worker count.
- **Statistical rigour:** report mean ± CI and sample size; for strategy comparisons prefer paired
  designs (same shuffled shoes for both strategies) to reduce variance.
- **Rules are config:** variants (decks, soft-17, payouts, penetration) are values, not subclasses.
- **Performance:** start simple and vectorised where natural; profile before optimising.
  Heavy inner loops can later move to numba or a compiled extension behind the same interfaces.
- **Testing:** unit tests for rules; seeded, tolerance-based statistical tests against known values
  (e.g. published Blackjack house edge for given rules) marked `statistical`/`slow`.
