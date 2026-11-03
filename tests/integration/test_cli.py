"""Every shipped Hydra config must compose and run."""

from pathlib import Path

import pandas as pd
import pytest
from hydra import compose, initialize_config_dir

from advantage_play.cli import CONF_DIR, run

PLAYERS = sorted(path.stem for path in (CONF_DIR / "players").glob("*.yaml"))


@pytest.mark.parametrize("players", PLAYERS)
def test_player_configs_run_end_to_end(players: str, tmp_path: Path) -> None:
    with initialize_config_dir(str(CONF_DIR), version_base="1.3"):
        cfg = compose("config", overrides=[f"players={players}", "n_games=50"])

    run(cfg, tmp_path)

    scores = pd.read_csv(tmp_path / "scores.csv", index_col="game")
    assert scores.shape == (50, len(cfg.players))
    assert list(scores.columns) == list(cfg.players)
    assert (tmp_path / "summary.csv").exists()
