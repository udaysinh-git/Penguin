"""
Configuration loader for Penguin Discord Bot.

- Loads from config/config.yaml if present.
- Otherwise, loads from .env file or environment variables.
- For each key: check config.yaml, then .env, then environment, else None.
"""

import os
import yaml
from pathlib import Path
from dotenv import load_dotenv

CONFIG_PATH = Path(__file__).parent / "config.yaml"
ENV_PATH = Path(__file__).parent.parent / ".env"

def _load_yaml_config():
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, "r") as f:
            return yaml.safe_load(f) or {}
    return {}

def _load_env():
    if ENV_PATH.exists():
        load_dotenv(dotenv_path=ENV_PATH)

def get_config_value(key: str):
    """
    Returns the value for a config key:
    1. config.yaml
    2. .env or environment variable
    3. None if not found
    """
    yaml_config = _load_yaml_config()
    if key in yaml_config:
        return yaml_config[key]
    _load_env()
    # Special case for Discord token: check both possible keys
    if key == "DISCORD_TOKEN":
        return os.getenv("DISCORD_TOKEN") or os.getenv("DISCORD_BOT_TOKEN")
    return os.getenv(key)

# Example usage for the Discord bot token
DISCORD_BOT_TOKEN = get_config_value("DISCORD_BOT_TOKEN")

SERVICE_FILTER_PATH = os.path.join(os.path.dirname(__file__), "service_filter.txt")

# Load .env if present
load_dotenv()

_missing_config_warnings = []

def _get_from_env_or_yaml(key, default=None):
    # Try config.yaml first
    config_path = os.path.join(os.path.dirname(__file__), "config.yaml")
    value = None
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
        if config and isinstance(config, dict):
            value = config.get(key)
    # Try .env/environment if not found in config.yaml
    if not value:
        value = os.getenv(key)
    # If still not found, use default
    if value is None or value == "":
        value = default
    _warn_if_missing(key, value)
    return value

def _warn_if_missing(key, value):
    # Treat 0, "0", None, and "" as missing
    if value is None or value == "" or value == 0 or value == "0":
        _missing_config_warnings.append(f"[CONFIG WARNING] Missing required config value: {key}")

SERVER_ID = _get_from_env_or_yaml("SERVER_ID", 0)
_warn_if_missing("SERVER_ID", SERVER_ID)
try:
    if SERVER_ID is not None and SERVER_ID != "":
        SERVER_ID = int(SERVER_ID)
    else:
        SERVER_ID = 0
except Exception:
    SERVER_ID = 0

ADMIN_ID = _get_from_env_or_yaml("ADMIN_ID", 0)
_warn_if_missing("ADMIN_ID", ADMIN_ID)
try:
    if ADMIN_ID is not None and ADMIN_ID != "":
        ADMIN_ID = int(ADMIN_ID)
    else:
        ADMIN_ID = 0
except Exception:
    ADMIN_ID = 0

def get_missing_config_warnings():
    return _missing_config_warnings
