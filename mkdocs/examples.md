# Examples

## Plain Text

```bash
slackit --webhook "$SLACK_WEBHOOK_URL" --text "Deploy finished"
```

## Username, Channel, and Icon

```bash
slackit \
  --webhook "$SLACK_WEBHOOK_URL" \
  --username PyBot \
  --channel "#testing" \
  --icon-emoji ":robot_face:" \
  --text "Hello, Slack!"
```

## Attachment

```bash
slackit --webhook "$SLACK_WEBHOOK_URL" --attachment \
  '{"fallback": "Required summary", "text": "Optional text inside the attachment"}'
```

## Block Kit

```bash
slackit --webhook "$SLACK_WEBHOOK_URL" --blocks \
  '[{"type": "section", "text": {"type": "mrkdwn", "text": "Hello from slackit"}}]'
```

## Validation Post

```bash
slackit --webhook "$SLACK_WEBHOOK_URL" --validate
```

This posts `This is a validation message` to channel `general`.

## Profiles

`$HOME/.slackit.yml`:

```yaml
profiles:
  testing:
    webhook_url: https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXX
    username: PyBot
    channel: "#testing"
    icon_emoji: ":robot_face:"
  alerts:
    webhook_url: https://hooks.slack.com/services/T00000000/B00000000/YYYYYYYY
    channel: "#alerts"
```

```bash
slackit --profile testing --text "Hello, Slack!"
slackit -p alerts --config "$HOME/work/slackit.yml" --text "Disk full"
slackit -p testing --channel "#other" --text "Override the profile channel"
```

## Library

```python
from lupaxa.slackit import Slackit, load_profile

profile = load_profile("alerts")
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
)
client.send_message("Hello\\nfrom the library")
```
