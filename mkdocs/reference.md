# Reference

## CLI arguments

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

The webhook URL must start with `https://hooks.slack.com/services/`.
`--timeout` must be greater than `0`. One of `--text`, `--attachment`,
`--blocks`, or `--validate` is required. Pass `--webhook`, or `--profile`
with a `webhook_url` in the config file. `--config` selects a file other
than `$HOME/.slackit.yml`. CLI flags override the selected profile.

## Config file

The default path is `$HOME/.slackit.yml`, from `default_config_path()`.
`--config` selects another file and requires `--profile`.

| Field         | Required                         | Meaning                                      |
| :------------ | :------------------------------- | :------------------------------------------- |
| `webhook_url` | unless `--webhook` is passed     | Slack incoming webhook URL                   |
| `username`    | no                               | Display name                                 |
| `channel`     | no                               | Channel override                             |
| `icon_emoji`  | no                               | Icon emoji                                   |
| `timeout`     | no                               | Request timeout in seconds; default `10`     |

The file must contain a `profiles` mapping. Profile names are strings.
Unknown keys are rejected. CLI flags override the selected profile.

## Exit codes

| Code | When                                                         |
| :--- | :----------------------------------------------------------- |
| `0`  | Help, version, or Slack accepted the post                    |
| `1`  | The webhook was rejected, or the post failed                 |
| `2`  | Command-line usage, a bad config, or argument parsing failed |

## Library

| Name                  | Meaning                                                       |
| :-------------------- | :------------------------------------------------------------ |
| `Slackit`             | Client bound to one incoming webhook                          |
| `send_message`        | Post text, unescaping `\\n`                                   |
| `send`                | Alias of `send_message`                                       |
| `send_attachment`     | Post one attachment from a JSON object string                 |
| `send_block`          | Post Block Kit blocks from a JSON string                      |
| `send_payload`        | POST a JSON object, filling username, channel, and icon emoji |
| `validate`            | HEAD the webhook, then post a validation message to `general` |
| `valid_webhook`       | Return whether a URL answers `HEAD` without a redirect        |
| `convert_to_json`     | Parse a JSON string or raise `ValueError`                     |
| `DEFAULT_TIMEOUT`     | Default request timeout (`10.0`)                              |
| `WEBHOOK_PREFIX`      | Required URL prefix                                           |
| `load_profile`        | Load one named profile from a YAML config file                |
| `default_config_path` | Return `$HOME/.slackit.yml`                                   |
| `ConfigError`         | Raised when the config file or profile cannot be used         |
| `Profile`             | Webhook settings stored for one profile                       |
| `get_version()`       | Return the package version string                             |

A Slack HTTP 200 response returns `True`. Redirects, an empty error body, Slack
error text, and invalid JSON raise `ValueError`. Network failures raise the
underlying `requests` exception. `validate` returns `False` when the follow-up
`HEAD` does not succeed.
