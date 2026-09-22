"""Slack incoming-webhook client."""

from __future__ import annotations

import json
import math

import requests

DEFAULT_TIMEOUT = 10.0
WEBHOOK_PREFIX = "https://hooks.slack.com/services/"
_REDIRECT_STATUSES = {301, 302}


class Slackit:
    """Send messages through a Slack incoming webhook."""

    def __init__(
        self,
        webhook_url: str,
        *,
        username: str | None = None,
        channel: str | None = None,
        icon_emoji: str | None = None,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> None:
        """Store webhook settings after the URL passes validation."""
        if not webhook_url:
            raise ValueError("Webhook URL required")
        if not webhook_url.startswith(WEBHOOK_PREFIX):
            raise ValueError(
                f"Invalid webhook URL: {webhook_url} - should start with {WEBHOOK_PREFIX}"
            )
        self.webhook_url = webhook_url
        self.username = username
        self.channel = channel
        self.icon_emoji = icon_emoji
        self.timeout = _require_timeout(timeout)
        if not self.valid_webhook(self.webhook_url):
            raise ValueError(
                f"Invalid webhook URL: {self.webhook_url} - please check your configuration"
            )

    def valid_webhook(self, url: str) -> bool:
        """Return whether ``url`` answers without a redirect."""
        try:
            response = requests.head(
                url,
                allow_redirects=False,
                timeout=self.timeout,
            )
        except requests.RequestException:
            return False
        return response.status_code not in _REDIRECT_STATUSES

    def send_message(self, text: str) -> bool:
        """Post ``text``, turning escaped newlines into real line breaks."""
        return self.send_payload({"text": text.replace("\\n", "\n")})

    def send(self, text: str) -> bool:
        """Post ``text``. Alias of ``send_message``."""
        return self.send_message(text)

    def send_attachment(self, attachment: str) -> bool:
        """Post one attachment encoded as a JSON object string."""
        return self.send_payload({"attachments": [self.convert_to_json(attachment)]})

    def send_block(self, block: str) -> bool:
        """Post Block Kit blocks encoded as a JSON string."""
        return self.send_payload({"blocks": self.convert_to_json(block)})

    def convert_to_json(self, json_string: str) -> object:
        """Parse ``json_string`` or raise ``ValueError``."""
        try:
            parsed: object = json.loads(json_string)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid json") from exc
        return parsed

    def send_payload(self, payload: dict[str, object]) -> bool:
        """POST ``payload`` as JSON, filling username, channel, and icon."""
        body = _with_defaults(payload, self.icon_emoji, self.username, self.channel)
        response = requests.post(
            self.webhook_url,
            headers={"Content-Type": "application/json"},
            json=body,
            timeout=self.timeout,
            allow_redirects=False,
        )
        if response.status_code == 200:
            return True
        if response.status_code in _REDIRECT_STATUSES:
            raise ValueError(
                f"Invalid webhook URL: {self.webhook_url} - please check your configuration"
            )
        if not response.text:
            raise ValueError(f"Unknown error for webhook URL: {self.webhook_url}")
        raise ValueError(response.text)

    def validate(self) -> bool:
        """Send a validation message to channel ``general`` when HEAD succeeds."""
        if not self.valid_webhook(self.webhook_url):
            return False
        self.channel = "general"
        self.send_message("This is a validation message")
        return True


def _require_timeout(timeout: float) -> float:
    if not math.isfinite(timeout) or timeout <= 0:
        raise ValueError("timeout must be greater than 0")
    return timeout


def _with_defaults(
    payload: dict[str, object],
    icon_emoji: str | None,
    username: str | None,
    channel: str | None,
) -> dict[str, object]:
    body = dict(payload)
    for key, value in (
        ("icon_emoji", icon_emoji),
        ("username", username),
        ("channel", channel),
    ):
        if key not in body and value is not None:
            body[key] = value
    return body
