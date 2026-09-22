# Getting started

## Requirements

- Python 3.13 or newer
- A Slack incoming webhook URL you are allowed to post to
- `requests` and `PyYAML`, installed with the package

## Install

```bash
pip install lupaxa-slackit
slackit --help
```

## First run

```bash
slackit --webhook "$SLACK_WEBHOOK_URL" --text "Hello, Slack!"
```

The command exits `0` when Slack accepts the message. Put the webhook URL in
the environment, or in a profile, rather than in shell history.

## Config file

Profiles live in `$HOME/.slackit.yml`. Pass `--config` when the file lives
somewhere else. `--config` requires `--profile`.

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
slackit --profile testing --text "Hello, Slack!"
slackit -p alerts --config "$HOME/work/slackit.yml" --text "Disk full"
```

Each profile may set `webhook_url`, `username`, `channel`, `icon_emoji`, and
`timeout`. A CLI flag overrides the same field from the profile.

Module entry point:

```bash
python -m lupaxa.slackit --version
```

### From source (development)

```bash
make init
make python-install-dev
slackit --version
```

## Makefile helpers

```bash
make init                 # clone makefile-skills into .makefiles/
make python-install-dev   # editable install with [dev]
make python-check         # lint + type + test
make mkdocs-serve         # local docs site
```
