<p align="center">
  <a href="https://github.com/lupaxa-notifications-toolbox">
    <img src="https://raw.githubusercontent.com/the-lupaxa-project/brand-assets/master/logos/organisations/notifications-toolbox/readme-logo.png" alt="Notifications Toolbox" />
  </a>
</p>

<h1 align="center">Slackit</h1>

Send Slack messages through an incoming webhook. Use it as a library or as the
`slackit` command. A successful post is Slack answering HTTP 200.

Requires Python 3.13 or newer. `requests` and `PyYAML` install with the package.

## Install

```bash
pip install lupaxa-slackit
slackit --help
```

## CLI

```bash
slackit --webhook "$SLACK_WEBHOOK_URL" --text "Hello, Slack!"
slackit --webhook "$SLACK_WEBHOOK_URL" --username PyBot --channel "#testing" \
  --icon-emoji ":robot_face:" --text "Hello, Slack!"
slackit --webhook "$SLACK_WEBHOOK_URL" --attachment \
  '{"fallback": "Required summary", "text": "Optional text inside the attachment"}'
slackit --webhook "$SLACK_WEBHOOK_URL" --blocks \
  '[{"type": "section", "text": {"type": "mrkdwn", "text": "Hello from slackit"}}]'
slackit --webhook "$SLACK_WEBHOOK_URL" --validate
slackit --profile testing --text "Hello, Slack!"
slackit -p alerts --config "$HOME/work/slackit.yml" --text "Disk full"
slackit -p testing --channel "#other" --text "Override the profile channel"
python -m lupaxa.slackit --version
```

The webhook URL must start with `https://hooks.slack.com/services/`. Put it in
the environment or a profile rather than in the command line when you can.
`--text`, `--attachment`, `--blocks`, and `--validate` are mutually exclusive,
and one of them is required. `--validate` posts `This is a validation message`
to channel `general`. Escaped newlines in `--text` are sent as real line
breaks, so `Hello\\nthere` arrives as two lines. Flags override the same fields
from the selected profile. `--timeout` must be greater than `0`.

| Flag                 | Default          | Description                                    |
| :------------------- | :--------------- | :--------------------------------------------- |
| `--webhook`, `-w`    | profile value    | Slack incoming webhook URL                     |
| `--profile`, `-p`    | —                | Profile name in the config file                |
| `--config`           | `~/.slackit.yml` | Config file path                               |
| `--text`, `-t`       | —                | Message text                                   |
| `--attachment`, `-a` | —                | Attachment JSON object                         |
| `--blocks`, `-b`     | —                | Block Kit JSON                                 |
| `--validate`         | —                | Send a validation message to channel `general` |
| `--username`, `-u`   | profile value    | Display name                                   |
| `--channel`, `-c`    | profile value    | Channel override                               |
| `--icon-emoji`, `-i` | profile value    | Icon emoji                                     |
| `--timeout`, `-T`    | `10`             | Request timeout in seconds                     |
| `--version`          | —                | Print the package version and exit             |

| Code | When                                                         |
| :--- | :----------------------------------------------------------- |
| `0`  | Help, version, or Slack accepted the post                    |
| `1`  | The webhook was rejected, or the post failed                 |
| `2`  | Command-line usage, a bad config, or argument parsing failed |

## Config

Profiles live in `$HOME/.slackit.yml`. Pass `--config` to use another file.
`--config` requires `--profile`. Without `--profile`, pass `--webhook`.

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
`timeout`. Unknown keys are rejected. The file must contain a `profiles`
mapping.

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
client.send_attachment('{"text": "Inside the attachment"}')
client.send_block('[{"type": "section", "text": {"type": "mrkdwn", "text": "Hello"}}]')
```

`send` is an alias of `send_message`. Username, channel, and icon emoji are
added to the JSON body when you set them and the payload does not already
include that field. `load_profile` reads `$HOME/.slackit.yml` when `path` is
omitted. A missing file, unknown profile, or invalid YAML raises `ConfigError`.

A Slack HTTP 200 response returns `True`. Redirects, an empty error body, Slack
error text, and invalid JSON raise `ValueError`. Network failures raise the
underlying `requests` exception. `validate` returns `False` when the follow-up
`HEAD` does not succeed.

## Development

```bash
make init
make python-install-dev
make python-check
```

<a href="https://github.com/the-lupaxa-project">
    <img src="https://raw.githubusercontent.com/the-lupaxa-project/brand-assets/master/logos/components/footer-for-child-orgs.svg" alt="The Lupaxa Project Footer" width="100%" />
</a>
