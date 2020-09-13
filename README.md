# cotd-telegram-bot

cringe of the day bot

## how to start

1. install python3
2. go to `cotd-telegram-bot` directory
3. run `pip3 install -r requirements.txt`
4. run `COTD_TELEGRAM_BOT_TOKEN=123:TOKEN python3 bot/main.py`
5. enjoy

## commands

| command   | inline | reply | description |
|-----------|--------|-------|-------------|
| /start    | ✅ | | Reply in chat with 'start' |
| /cringe   | ✅ | ✅ | Post or reply smileyOne sticker |
| /iscringe | | ✅ | Validate message for cringe or base |
| /oldfellow | ✅ | | Reply with oldfellow gif |
| /kekw | ✅ | | Reply with KEKW gif |

## flow

1. start bot with accepted channelid/channelname flag in gcs and initialized as can-join-groups
   1. setwebhook method <https://core.telegram.org/bots/api#setwebhook>
   2.
2. /cotd will list all messages for the last day and select one which is cringe semi-randomly
3. then it will post smiley-cat as a reply
4. encode and send smiley-cat <https://core.telegram.org/bots/api#sendsticker>

## todo

* inline mode 'that's cringe'?

## stories

- As a shitposter I want to activate cringebot by sending a sticker so I can save up time typing "/cringe".
- As a shitposter I want to choose the bot activation sticker so I can add it a personal touch.
- As a shitposter I want to receive system feedback after calling the cringe so I can know that everything worked.
