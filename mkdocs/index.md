# Slackit

`lupaxa-slackit` posts messages to Slack through an incoming webhook. Use it as
a library or as the `slackit` command.

```bash
pip install lupaxa-slackit
slackit --webhook "$SLACK_WEBHOOK_URL" --text "Hello, Slack!"
slackit --profile testing --text "Hello, Slack!"
```

A successful post returns when Slack answers HTTP 200. The webhook URL must
start with `https://hooks.slack.com/services/`. `--profile` reads a named
profile from `$HOME/.slackit.yml`.
