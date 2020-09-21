# cotd-telegram-bot

cringe of the day bot

## how to start

1. install python3
2. export `COTD_TELEGRAM_BOT_TOKEN=` and run

```bash
    bazel run //cotd:cotdbot
```

## flow

1. start bot with accepted channelid/channelname flag in gcs and initialized as can-join-groups
   1. setwebhook method <https://core.telegram.org/bots/api#setwebhook> if not in token mode
2. /cotd will list all messages for the last day and select one which is cringe semi-randomly
   1. this will require database persistence
3. then it will post smiley-cat as a reply
   1. this will require database persistence

## todo

- inline mode 'that's cringe'?

## stories

- As a shitposter I want to activate cringebot by sending a sticker so I can save up time typing "/cringe".
- As a shitposter I want to choose the bot activation sticker so I can add it a personal touch.

### deploy

git push heroku master
