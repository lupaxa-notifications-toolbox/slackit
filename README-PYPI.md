<!-- markdownlint-disable -->
<p align="center">
  <a href="https://github.com/lupaxa-notifications-toolbox">
    <img src="https://raw.githubusercontent.com/the-lupaxa-project/brand-assets/master/logos/organisations/notifications-toolbox/readme-logo.png" alt="Project Logo" width="256"/><br/>
  </a>
</p>
<h3 align="center">
  The Lupaxa Notifications Toolbox<br />
  Part of The Lupaxa Project
</h3>

<br />

# lupaxa-slackit

Send Slack messages through an incoming webhook.

## Features

- Post message text, one attachment, or Block Kit blocks
- Set a username, channel, and icon emoji on each client
- Keep several webhook profiles in `$HOME/.slackit.yml` and select one with `--profile`
- Override any profile field with a CLI flag
- Turn escaped `\n` sequences in message text into real line breaks
- Reject webhook URLs that do not start with `https://hooks.slack.com/services/`
- Reject webhook URLs that answer `HEAD` with a redirect
- Use the `Slackit` library class or the `slackit` command

## Installation

### From PyPI

```bash
pip install lupaxa-slackit
```

### From source (development mode)

```bash
pip install -e ".[dev]"
```

Requires Python 3.13+. Runtime dependencies: `requests` and `PyYAML`.

## Library quick start

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
)
client.send_message("Hello, Slack!")
client.send_attachment('{"text": "Optional text inside the attachment"}')
client.send_block('[{"type": "section", "text": {"type": "mrkdwn", "text": "Hello"}}]')
```

## CLI quick start

```bash
slackit --help
slackit --webhook "$SLACK_WEBHOOK_URL" --text "Hello, Slack!"
slackit --profile testing --text "Hello, Slack!"
slackit -p alerts --config "$HOME/work/slackit.yml" --text "Disk full"
```

You can also run the CLI as a module:

```bash
python -m lupaxa.slackit --help
python -m lupaxa.slackit --version
```

## Config

Profiles live in one YAML file. The default path is `$HOME/.slackit.yml`.
Pass `--config` when the file lives somewhere else. `--config` requires
`--profile`. CLI flags override the selected profile.

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
`timeout`. `--webhook` is required when you do not pass `--profile`.

## Options

- `--webhook`, `-w`: Slack incoming webhook URL; required when `--profile` is omitted
- `--profile`, `-p`: profile name in the config file
- `--config`: config file path; default `$HOME/.slackit.yml`
- `--text`, `-t`: message text
- `--attachment`, `-a`: one attachment as a JSON object
- `--blocks`, `-b`: Block Kit payload as JSON
- `--validate`: send a validation message to channel `general`
- `--username`, `-u`: display name
- `--channel`, `-c`: channel override
- `--icon-emoji`, `-i`: icon emoji
- `--timeout`, `-T`: request timeout in seconds; default `10`
- `--version`: print the package version

`--text`, `--attachment`, `--blocks`, and `--validate` are mutually exclusive.
One of them is required. CLI flags override the selected profile.

## Documentation

Online documentation:

[Documentation](https://slackit.thelupaxaproject.org/)

Source repository:

[GitHub](https://github.com/lupaxa-notifications-toolbox/slackit)

### Serve docs locally

From a clone of the repository:

```bash
make mkdocs-serve
```

Then open the local URL printed by MkDocs in your browser.

## Development

Clone the repository and install with Make:

```bash
make init                # first-time makefile-skills checkout
make python-install-dev  # editable install with [dev]
make python-check        # lint, type-check, and test
```

<a href="https://github.com/the-lupaxa-project">
    <img src="https://raw.githubusercontent.com/the-lupaxa-project/brand-assets/master/logos/components/footer-for-child-orgs.svg" alt="The Lupaxa Project Footer" width="100%" />
</a>
