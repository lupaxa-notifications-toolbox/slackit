"""CLI entrypoint."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from lupaxa.slackit.cli import _program_name, build_parser, main
from lupaxa.slackit.version import get_version

WEBHOOK = "https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXX"
_BASE = ["--webhook", WEBHOOK]


def test_help_exits_zero(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["--help"]) == 0
    assert "--webhook" in capsys.readouterr().out


def test_version_flag(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["--version"]) == 0
    assert get_version() in capsys.readouterr().out


def test_missing_webhook_exits_two(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["--text", "hi"]) == 2
    assert "webhook URL required" in capsys.readouterr().err


def test_missing_mode_exits_two() -> None:
    assert main(_BASE) == 2


def test_parser_defaults() -> None:
    args = build_parser().parse_args([*_BASE, "--text", "hi"])
    assert args.webhook == WEBHOOK
    assert args.text == "hi"
    assert args.timeout is None
    assert args.profile is None
    assert args.username is None
    overridden = build_parser().parse_args([*_BASE, "--text", "hi", "--timeout", "2.5"])
    assert overridden.timeout == 2.5


def test_timeout_must_be_a_number() -> None:
    with pytest.raises(SystemExit):
        build_parser().parse_args([*_BASE, "--text", "hi", "--timeout", "nope"])


def test_text_calls_send_message() -> None:
    client = MagicMock()
    with patch("lupaxa.slackit.cli.Slackit", return_value=client) as ctor:
        assert main([*_BASE, "--username", "PyBot", "--text", "hi"]) == 0
    ctor.assert_called_once_with(
        WEBHOOK,
        username="PyBot",
        channel=None,
        icon_emoji=None,
        timeout=10.0,
    )
    client.send_message.assert_called_once_with("hi")


def test_attachment_and_blocks() -> None:
    client = MagicMock()
    with patch("lupaxa.slackit.cli.Slackit", return_value=client):
        assert main([*_BASE, "--attachment", "{}"]) == 0
        assert main([*_BASE, "--blocks", "[]"]) == 0
    client.send_attachment.assert_called_once_with("{}")
    client.send_block.assert_called_once_with("[]")


def test_profile_fills_client_and_flags_override(tmp_path: Path) -> None:
    path = tmp_path / "slackit.yml"
    path.write_text(
        "\n".join(
            [
                "profiles:",
                "  testing:",
                f"    webhook_url: {WEBHOOK}",
                "    username: PyBot",
                '    channel: "#testing"',
                '    icon_emoji: ":robot_face:"',
                "    timeout: 15",
            ],
        ),
        encoding="utf-8",
    )
    client = MagicMock()
    with patch("lupaxa.slackit.cli.Slackit", return_value=client) as ctor:
        assert main(["-p", "testing", "--config", str(path), "-c", "#other", "--text", "hi"]) == 0
    ctor.assert_called_once_with(
        WEBHOOK,
        username="PyBot",
        channel="#other",
        icon_emoji=":robot_face:",
        timeout=15.0,
    )


def test_unknown_profile_exits_two(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    path = tmp_path / "slackit.yml"
    path.write_text(
        f"profiles:\n  testing:\n    webhook_url: {WEBHOOK}\n",
        encoding="utf-8",
    )
    assert main(["-p", "missing", "--config", str(path), "--text", "hi"]) == 2
    assert "profile not found" in capsys.readouterr().err


def test_validate_success_and_failure() -> None:
    client = MagicMock()
    client.validate.return_value = True
    with patch("lupaxa.slackit.cli.Slackit", return_value=client):
        assert main([*_BASE, "--validate"]) == 0
    client.validate.return_value = False
    with patch("lupaxa.slackit.cli.Slackit", return_value=client):
        assert main([*_BASE, "--validate"]) == 1


def test_value_error_uses_program_prefix(capsys: pytest.CaptureFixture[str]) -> None:
    with (
        patch("lupaxa.slackit.cli.Slackit", side_effect=ValueError("bad webhook")),
        patch("lupaxa.slackit.cli.sys.argv", ["/path/to/slackit"]),
    ):
        assert main([*_BASE, "--text", "hi"]) == 1
    assert capsys.readouterr().err == "slackit: bad webhook\n"


@pytest.mark.parametrize(
    ("argv0", "expected"),
    [
        ("/path/to/slackit", "slackit"),
        ("/path/to/__main__.py", "slackit"),
    ],
)
def test_program_name(argv0: str, expected: str) -> None:
    assert _program_name(argv0) == expected


def test_timeout_flag_rejected() -> None:
    with pytest.raises(SystemExit):
        build_parser().parse_args([*_BASE, "--text", "hi", "--timeout", "0"])
