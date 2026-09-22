"""Slackit client."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest
import requests

from lupaxa.slackit.client import WEBHOOK_PREFIX, Slackit

WEBHOOK = f"{WEBHOOK_PREFIX}T00000000/B00000000/XXXXXXXX"


def _response(status: int, text: str = "ok") -> MagicMock:
    response = MagicMock()
    response.status_code = status
    response.text = text
    return response


def _client(**kwargs: object) -> Slackit:
    with patch("lupaxa.slackit.client.requests.head", return_value=_response(200)):
        return Slackit(WEBHOOK, **kwargs)  # type: ignore[arg-type]


def test_missing_webhook_raises() -> None:
    with pytest.raises(ValueError, match="Webhook URL required"):
        Slackit("")


def test_prefix_is_required() -> None:
    with pytest.raises(ValueError, match="should start with"):
        Slackit("https://example.com/hook")


def test_redirect_on_head_is_rejected() -> None:
    with (
        patch("lupaxa.slackit.client.requests.head", return_value=_response(302)),
        pytest.raises(ValueError, match="please check your configuration"),
    ):
        Slackit(WEBHOOK)


def test_head_error_is_rejected() -> None:
    with (
        patch(
            "lupaxa.slackit.client.requests.head",
            side_effect=requests.ConnectionError("down"),
        ),
        pytest.raises(ValueError, match="please check your configuration"),
    ):
        Slackit(WEBHOOK)


def test_send_message_posts_text_and_defaults() -> None:
    client = _client(username="PyBot", channel="#testing", icon_emoji=":robot_face:")
    with patch(
        "lupaxa.slackit.client.requests.post",
        return_value=_response(200),
    ) as post:
        assert client.send_message("Hello\\nthere") is True
    body = post.call_args.kwargs["json"]
    assert body["text"] == "Hello\nthere"
    assert body["username"] == "PyBot"
    assert body["channel"] == "#testing"
    assert body["icon_emoji"] == ":robot_face:"
    assert post.call_args.kwargs["allow_redirects"] is False


def test_send_is_alias() -> None:
    client = _client()
    with patch.object(client, "send_message", return_value=True) as send_message:
        assert client.send("hi") is True
    send_message.assert_called_once_with("hi")


def test_send_attachment_and_blocks() -> None:
    client = _client()
    with patch(
        "lupaxa.slackit.client.requests.post",
        return_value=_response(200),
    ) as post:
        assert client.send_attachment('{"text": "inside"}') is True
        assert client.send_block('[{"type": "section"}]') is True
    attachment, blocks = (call.kwargs["json"] for call in post.call_args_list)
    assert attachment["attachments"] == [{"text": "inside"}]
    assert blocks["blocks"] == [{"type": "section"}]


def test_invalid_json_raises() -> None:
    client = _client()
    with pytest.raises(ValueError, match="Invalid json"):
        client.send_attachment("not-json")


def test_payload_values_win_over_defaults() -> None:
    client = _client(username="PyBot")
    with patch(
        "lupaxa.slackit.client.requests.post",
        return_value=_response(200),
    ) as post:
        client.send_payload({"text": "hi", "username": "Other"})
    assert post.call_args.kwargs["json"]["username"] == "Other"


def test_omits_unset_defaults() -> None:
    client = _client()
    with patch(
        "lupaxa.slackit.client.requests.post",
        return_value=_response(200),
    ) as post:
        client.send_message("hi")
    body = post.call_args.kwargs["json"]
    assert "username" not in body
    assert "channel" not in body
    assert "icon_emoji" not in body


@pytest.mark.parametrize(
    ("status", "text", "match"),
    [
        (302, "", "please check your configuration"),
        (500, "", "Unknown error"),
        (400, "invalid_payload", "invalid_payload"),
    ],
)
def test_post_errors(status: int, text: str, match: str) -> None:
    client = _client()
    with (
        patch(
            "lupaxa.slackit.client.requests.post",
            return_value=_response(status, text),
        ),
        pytest.raises(ValueError, match=match),
    ):
        client.send_message("hi")


def test_request_exception_propagates() -> None:
    client = _client()
    with (
        patch(
            "lupaxa.slackit.client.requests.post",
            side_effect=requests.Timeout("slow"),
        ),
        pytest.raises(requests.Timeout),
    ):
        client.send_message("hi")


def test_validate_sends_to_general() -> None:
    client = _client(channel="#testing")
    with (
        patch("lupaxa.slackit.client.requests.head", return_value=_response(200)),
        patch(
            "lupaxa.slackit.client.requests.post",
            return_value=_response(200),
        ) as post,
    ):
        assert client.validate() is True
    body = post.call_args.kwargs["json"]
    assert body["text"] == "This is a validation message"
    assert body["channel"] == "general"


def test_validate_false_when_head_fails() -> None:
    client = _client()
    with patch.object(client, "valid_webhook", return_value=False):
        assert client.validate() is False


def test_timeout_must_be_positive() -> None:
    with pytest.raises(ValueError, match="timeout must be greater than 0"):
        _client(timeout=0)
