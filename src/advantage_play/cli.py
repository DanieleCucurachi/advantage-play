"""Command-line entry point, configured with Hydra (see ``conf/``)."""

import logging
from pathlib import Path

import hydra
import pandas as pd
from hydra.core.hydra_config import HydraConfig
from hydra.utils import instantiate
from omegaconf import DictConfig

from advantage_play.analysis import paired_difference, summarize
from advantage_play.simulation import simulate

log = logging.getLogger(__name__)

# The repo's config tree (works from a clone installed with `uv sync`).
CONF_DIR = Path(__file__).resolve().parents[2] / "conf"


def run(cfg: DictConfig, output_dir: Path) -> None:
    """Simulate the configured experiment, log the report and save the results to ``output_dir``."""
    game = instantiate(cfg.game)
    players = instantiate(cfg.players, _convert_="all")  # {label: strategy}, in seat order
    labels = list(players)

    scores = simulate(game, list(players.values()), cfg.n_games, cfg.seed)
    summary = summarize(scores, labels, cfg.confidence)

    pd.DataFrame(scores, columns=labels).to_csv(output_dir / "scores.csv", index_label="game")
    summary.to_csv(output_dir / "summary.csv")
    log.info("Results over %d games\n%s", cfg.n_games, summary.round(4).to_string())
    if len(labels) > 1:
        diff = paired_difference(scores, labels, cfg.confidence)
        log.info("Score difference vs '%s' (paired)\n%s", labels[0], diff.round(4).to_string())


@hydra.main(config_path=str(CONF_DIR), config_name="config", version_base="1.3")
def main(cfg: DictConfig) -> None:
    """Run the experiment described by the Hydra config."""
    run(cfg, Path(HydraConfig.get().runtime.output_dir))
