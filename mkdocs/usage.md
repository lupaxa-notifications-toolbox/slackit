# Usage

Use `slackit` to post one message, one attachment, or one Block Kit payload.
Pass the webhook URL with `--webhook`, or select a profile with `--profile`.

## CLI flags

| Flag                 | Default            | Description                                      |
| :------------------- | :----------------- | :----------------------------------------------- |
| `--webhook`, `-w`    | profile value      | Slack incoming webhook URL                       |
| `--profile`, `-p`    | —                  | Profile name in the config file                  |
| `--config`           | `~/.slackit.yml`   | Config file path                                 |
| `--text`, `-t`       | —                  | Message text                                     |
| `--attachment`, `-a` | —                  | Attachment JSON object                           |
| `--blocks`, `-b`     | —                  | Block Kit JSON                                   |
| `--validate`         | —                  | Send a validation message to channel `general`   |
| `--username`, `-u`   | profile value      | Display name                                     |
| `--channel`, `-c`    | profile value      | Channel override                                 |
| `--icon-emoji`, `-i` | profile value      | Icon emoji                                       |
| `--timeout`, `-T`    | `10`               | Request timeout in seconds                       |
| `--version`          | —                  | Print the package version and exit               |

```bash
slackit --webhook "$SLACK_WEBHOOK_URL" --username PyBot --channel "#testing" --text "Hello"
```

`--text`, `--attachment`, `--blocks`, and `--validate` are mutually exclusive.
One of them is required. `--timeout` must be greater than `0`. A flag overrides
the same field from the selected profile.

## Config file

Profiles live in one YAML file. The default path is `$HOME/.slackit.yml`.
Pass `--config` when the file lives somewhere else.

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

```bash
slackit --profile testing --text "Hello"
slackit -p alerts --config "$HOME/work/slackit.yml" --text "Disk full"
```

Each profile may set `webhook_url`, `username`, `channel`, `icon_emoji`, and
`timeout`. Other keys are rejected. `--webhook` is still required when you
do not pass `--profile`. `--config` requires `--profile`.

Escaped newlines in `--text` are sent as real line breaks, so `Hello\\nthere`
arrives as two lines.

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
client.send_message("Hello from a profile")

client = Slackit(
    "https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXX",
    username="PyBot",
    channel="#testing",
    icon_emoji=":robot_face:",
    timeout=10.0,
)
client.send_message("Hello, Slack!")
client.send("Hello, Slack!")
client.send_attachment('{"text": "Inside the attachment"}')
client.send_block('[{"type": "section", "text": {"type": "mrkdwn", "text": "Hello"}}]')
```

`send` is an alias of `send_message`. Username, channel, and icon emoji are
added to the JSON body when you set them and the payload does not already
include that field. `validate` checks the webhook again and posts
`This is a validation message` to channel `general`.

Signatures:

```python
Slackit(
    webhook_url: str,
    *,
    username: str | None = None,
    channel: str | None = None,
    icon_emoji: str | None = None,
    timeout: float = 10.0,
)

send_message(text: str) -> bool
send(text: str) -> bool
send_attachment(attachment: str) -> bool
send_block(block: str) -> bool
send_payload(payload: dict[str, object]) -> bool
validate() -> bool

load_profile(name: str, path: Path | None = None) -> Profile
```

`load_profile` reads `$HOME/.slackit.yml` when `path` is omitted. A missing
file, unknown profile, or invalid YAML raises `ConfigError`.
