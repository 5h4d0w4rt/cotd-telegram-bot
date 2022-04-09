#! python3
# dump database from file_id and token
import sys
import json
import gzip
import telegram

if __name__ == '__main__':
    bot = telegram.Bot(token=sys.argv[1])
    file = bot.get_file(file_id=sys.argv[2])

    print(json.dumps(json.loads(gzip.decompress(file.download_as_bytearray())), indent=2))
