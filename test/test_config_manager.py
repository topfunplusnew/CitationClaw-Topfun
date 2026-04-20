"""Unit tests for ConfigManager runtime path behavior."""
import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from citationclaw.app.config_manager import ConfigManager


def test_config_manager_defaults_to_local_config_name():
    old = os.environ.pop("CITATIONCLAW_CONFIG_PATH", None)
    try:
        manager = ConfigManager()
        assert manager.config_path == Path("config.json")
    finally:
        if old is not None:
            os.environ["CITATIONCLAW_CONFIG_PATH"] = old


def test_config_manager_uses_env_override():
    cfg = Path(tempfile.mkdtemp()) / "runtime" / "config.json"
    old = os.environ.get("CITATIONCLAW_CONFIG_PATH")
    os.environ["CITATIONCLAW_CONFIG_PATH"] = str(cfg)
    try:
        manager = ConfigManager()
        assert manager.config_path == cfg
    finally:
        if old is None:
            os.environ.pop("CITATIONCLAW_CONFIG_PATH", None)
        else:
            os.environ["CITATIONCLAW_CONFIG_PATH"] = old
