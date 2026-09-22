<p align="center">
  <a href="https://github.com/lupaxa-notifications-toolbox">
    <img src="https://raw.githubusercontent.com/the-lupaxa-project/brand-assets/master/logos/organisations/notifications-toolbox/readme-logo.png" alt="Notifications Toolbox" />
  </a>
</p>

<h1 align="center">slackit</h1>

Send Slack messages through an incoming webhook.

<p align="center">
  <a href="https://slackit.thelupaxaproject.org/">Documentation</a>
  ·
  <a href="https://github.com/lupaxa-notifications-toolbox/slackit">GitHub</a>
</p>

## Install

```bash
pip install lupaxa-slackit
slackit --help
```

## CLI

```bash
slackit --webhook "$SLACK_WEBHOOK_URL" --text "Hello, Slack!"
slackit --profile testing --text "Hello, Slack!"
slackit -p alerts --config "$HOME/work/slackit.yml" --text "Disk full"
python -m lupaxa.slackit --version
```

The webhook URL must start with `https://hooks.slack.com/services/`.
`--text`, `--attachment`, `--blocks`, and `--validate` are mutually exclusive.
Flags override the same fields from the selected profile.

## Config

Profiles live in `$HOME/.slackit.yml`. Pass `--config` to use another file.
`--config` requires `--profile`.

```yaml
profiles:
  testing:
    webhook_url: https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXX
    username: PyBot
    channel: "#testing"
    icon_emoji: ":robot_face:"
    timeout: 15
  alerts:
    webhook_url: https://hooks.slack.com/services/T00000000/B00000000/YYYYYYYY
    channel: "#alerts"
```

Each profile may set `webhook_url`, `username`, `channel`, `icon_emoji`, and
`timeout`.

## Library

```python
from lupaxa.slackit import Slackit, load_profile

profile = load_profile("testing")
client = Slackit(
    profile.webhook_url,
    username=profile.username,
    channel=profile.channel,
    icon_emoji=profile.icon_emoji,
)
client.send_message("Hello, Slack!")
```

## Development

```bash
make init
make python-install-dev
make python-check
make mkdocs-serve
```

<a href="https://github.com/the-lupaxa-project">
    <img src="https://raw.githubusercontent.com/the-lupaxa-project/brand-assets/master/logos/components/footer-for-child-orgs.svg" alt="The Lupaxa Project Footer" width="100%" />
</a>
