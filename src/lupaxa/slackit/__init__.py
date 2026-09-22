"""lupaxa.slackit — send Slack messages through an incoming webhook."""

from __future__ import annotations

from .client import DEFAULT_TIMEOUT, WEBHOOK_PREFIX, Slackit
from .config import ConfigError, Profile, default_config_path, load_profile
from .version import __version__, get_version

__all__ = [
    "DEFAULT_TIMEOUT",
    "WEBHOOK_PREFIX",
    "ConfigError",
    "Profile",
    "Slackit",
    "__version__",
    "default_config_path",
    "get_version",
    "load_profile",
]
