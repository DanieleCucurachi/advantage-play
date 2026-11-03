from pathlib import Path

import pytest
from hydra import compose, initialize_config_dir
from omegaconf import MissingMandatoryValue, OmegaConf

CONFIG_DIR = str(Path(__file__).resolve().parents[1] / "configs")


def test_default_configuration() -> None:
    with initialize_config_dir(config_dir=CONFIG_DIR, version_base="1.3"):
        config = compose(config_name="config")

    assert OmegaConf.is_missing(config.game, "name")
    assert OmegaConf.is_missing(config.strategy, "name")
    assert len(set(config.game.deck.suits)) == 4
    assert len(set(config.game.deck.ranks)) == 13
    assert all(isinstance(rank, str) for rank in config.game.deck.ranks)
    assert config.game.deck.copies == 1
    assert config.simulation.seed == 42
    assert config.simulation.episodes == 10000
    assert config.simulation.repetitions == 10
    assert config.reporting.confidence_level == 0.95
    assert config.reporting.save_raw_results is True
    with pytest.raises(MissingMandatoryValue):
        OmegaConf.to_container(config, resolve=True, throw_on_missing=True)


def test_experiment_preset_and_overrides() -> None:
    with initialize_config_dir(config_dir=CONFIG_DIR, version_base="1.3"):
        config = compose(
            config_name="config",
            overrides=[
                "experiment=smoke",
                "game.name=example",
                "strategy.name=example",
                "simulation.seed=7",
                "+game.rules.example_rule=true",
                "+strategy.parameters.example_parameter=2",
            ],
        )

    resolved = OmegaConf.to_container(config, resolve=True, throw_on_missing=True)
    assert resolved["game"]["name"] == "example"
    assert resolved["strategy"]["name"] == "example"
    assert config.game.rules.example_rule is True
    assert config.strategy.parameters.example_parameter == 2
    assert config.simulation.episodes == 100
    assert config.simulation.repetitions == 2
    assert config.simulation.seed == 7
    assert "experiment" not in config


def test_hydra_output_configuration() -> None:
    with initialize_config_dir(config_dir=CONFIG_DIR, version_base="1.3"):
        config = compose(config_name="config", return_hydra_config=True)

    assert config.hydra.job.chdir is False
    assert config.hydra.run.dir.startswith("outputs/")
    assert config.hydra.sweep.dir.startswith("multirun/")
    assert OmegaConf.to_container(config.hydra.sweep)["subdir"] == "${hydra.job.num}"
