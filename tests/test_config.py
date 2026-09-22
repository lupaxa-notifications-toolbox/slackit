"""YAML profile config."""

from __future__ import annotations

from pathlib import Path

import pytest

from lupaxa.slackit.config import (
    ConfigError,
    default_config_path,
    load_profile,
    resolve_settings,
)

WEBHOOK = "https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXX"
OTHER = "https://hooks.slack.com/services/T00000000/B00000000/YYYYYYYY"

_FILE = f"""
profiles:
  testing:
    webhook_url: {WEBHOOK}
    username: PyBot
    channel: "#testing"
    icon_emoji: ":robot_face:"
    timeout: 15
  alerts:
    webhook_url: {OTHER}
    channel: "#alerts"
"""


def test_default_config_path_is_home_dotfile(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    assert default_config_path() == tmp_path / ".slackit.yml"


def test_load_profile_uses_home_by_default(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    (tmp_path / ".slackit.yml").write_text(_FILE, encoding="utf-8")
    assert load_profile("testing").webhook_url == WEBHOOK


def test_load_profile(tmp_path: Path) -> None:
    path = tmp_path / ".slackit.yml"
    path.write_text(_FILE, encoding="utf-8")
    profile = load_profile("testing", path)
    assert profile.webhook_url == WEBHOOK
    assert profile.username == "PyBot"
    assert profile.channel == "#testing"
    assert profile.icon_emoji == ":robot_face:"
    assert profile.timeout == 15.0
    alerts = load_profile("alerts", path)
    assert alerts.username is None
    assert alerts.timeout is None


def test_missing_file(tmp_path: Path) -> None:
    with pytest.raises(ConfigError, match="config file not found"):
        load_profile("testing", tmp_path / "missing.yml")


def test_unknown_profile(tmp_path: Path) -> None:
    path = tmp_path / ".slackit.yml"
    path.write_text(_FILE, encoding="utf-8")
    with pytest.raises(ConfigError, match="profile not found: missing"):
        load_profile("missing", path)


def test_invalid_yaml(tmp_path: Path) -> None:
    path = tmp_path / ".slackit.yml"
    path.write_text("profiles: [\n", encoding="utf-8")
    with pytest.raises(ConfigError, match="invalid config file"):
        load_profile("testing", path)


def test_unknown_setting(tmp_path: Path) -> None:
    path = tmp_path / ".slackit.yml"
    path.write_text(
        f"profiles:\n  testing:\n    webhook_url: {WEBHOOK}\n    token: secret\n",
        encoding="utf-8",
    )
    with pytest.raises(ConfigError, match="unknown profile setting: token"):
        load_profile("testing", path)


def test_resolve_profile_and_cli_override(tmp_path: Path) -> None:
    path = tmp_path / ".slackit.yml"
    path.write_text(_FILE, encoding="utf-8")
    settings = resolve_settings(
        profile_name="testing",
        config_path=path,
        webhook_url=None,
        username=None,
        channel="#other",
        icon_emoji=None,
        timeout=None,
    )
    assert settings.webhook_url == WEBHOOK
    assert settings.username == "PyBot"
    assert settings.channel == "#other"
    assert settings.icon_emoji == ":robot_face:"
    assert settings.timeout == 15.0


def test_resolve_without_profile_uses_timeout_default() -> None:
    settings = resolve_settings(
        profile_name=None,
        config_path=None,
        webhook_url=WEBHOOK,
        username=None,
        channel=None,
        icon_emoji=None,
        timeout=None,
    )
    assert settings.timeout == 10.0


def test_config_without_profile_is_rejected(tmp_path: Path) -> None:
    with pytest.raises(ConfigError, match="--profile is required"):
        resolve_settings(
            profile_name=None,
            config_path=tmp_path / ".slackit.yml",
            webhook_url=WEBHOOK,
            username=None,
            channel=None,
            icon_emoji=None,
            timeout=None,
        )


def test_cli_timeout_overrides_profile(tmp_path: Path) -> None:
    path = tmp_path / ".slackit.yml"
    path.write_text(_FILE, encoding="utf-8")
    settings = resolve_settings(
        profile_name="testing",
        config_path=path,
        webhook_url=OTHER,
        username="Other",
        channel=None,
        icon_emoji=None,
        timeout=3,
    )
    assert settings.webhook_url == OTHER
    assert settings.username == "Other"
    assert settings.timeout == 3


@pytest.mark.parametrize(
    ("text", "match"),
    [
        ("profiles: {}\n", "must define profiles"),
        ("note: hi\nprofiles:\n  testing:\n    webhook_url: x\n", "unknown config setting"),
        ("[]\n", "invalid config file"),
        (
            "profiles:\n  testing:\n    webhook_url: x\n    timeout: 0\n",
            "timeout must be greater than 0",
        ),
        (
            'profiles:\n  testing:\n    webhook_url: ""\n',
            "webhook_url must be a non-empty string",
        ),
    ],
)
def test_rejected_config_shapes(tmp_path: Path, text: str, match: str) -> None:
    path = tmp_path / ".slackit.yml"
    path.write_text(text, encoding="utf-8")
    with pytest.raises(ConfigError, match=match):
        load_profile("testing", path)


def test_missing_webhook_is_rejected() -> None:
    with pytest.raises(ConfigError, match="webhook URL required"):
        resolve_settings(
            profile_name=None,
            config_path=None,
            webhook_url=None,
            username=None,
            channel=None,
            icon_emoji=None,
            timeout=None,
        )
