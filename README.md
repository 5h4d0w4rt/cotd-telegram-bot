# cotd-telegram-bot

cringe of the day bot

## how to start

1. install python3 ([pyenv](https://github.com/pyenv/pyenv) preferred)
2. get bazelisk

```bash

   brew install bazelisk
```

3. export `COTD_TELEGRAM_BOT_TOKEN=`[how to get bot](https://core.telegram.org/bots) and run

```bash

   bazelisk test //...
   bazelisk run //cotd:cotdbot
```

## interactive shell

1. install poetry - pipx install poetry
2. poetry install
3. poetry shell

## plumbing

### inspect database

bazel run --ui_event_filters=-info,-stdout,-stderr --noshow_progress //hack:inspect_db $TOKEN file_id_corresponding_to_bot

## flow

1. start bot with accepted channelid/channelname flag in gcs and initialized as can-join-groups
   1. setwebhook method <https://core.telegram.org/bots/api#setwebhook> if not in token mode
2. /cotd will list all messages for the last day and select one which is cringe semi-randomly
   1. this will require database persistence
3. then it will post smiley-cat as a reply
   1. this will require database persistence

## stories

- As a shitposter I want to activate cringebot by sending a sticker so I can save up time typing "/cringe".
- As a shitposter I want to choose the bot activation sticker so I can add it a personal touch.

### deploy

by github action

```

```
