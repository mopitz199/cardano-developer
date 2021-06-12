# save this as app.py

import requests
import redis
import os

from discord import Webhook, RequestsWebhookAdapter
from flask import Flask

from bot.services import get_num_of_block_last_epoch, get_last_epoch_number, get_message

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

from dotenv import load_dotenv  # dotenv to handle env variables in a .env file
load_dotenv()  # load the .env file


@app.cli.command()
def send_pool_info():
    url = os.environ.get("DISCORD_REPORT_EPOCH_WEBHOOK_URL")
    webhook = Webhook.from_url(url, adapter=RequestsWebhookAdapter())

    last_epoch_number = get_last_epoch_number()
    num_of_block_last_epoch = get_num_of_block_last_epoch()

    print(f"{url}, {last_epoch_number}; {num_of_block_last_epoch}")
    cached_num_of_block_last_epoch = cache.get('num_of_block_last_epoch')
    if cached_num_of_block_last_epoch is not None:
        cached_num_of_block_last_epoch = cached_num_of_block_last_epoch.decode()
        cached_num_of_block_last_epoch = int(cached_num_of_block_last_epoch)

    if (
        cached_num_of_block_last_epoch is None or
        cached_num_of_block_last_epoch != num_of_block_last_epoch
    ):
        cache.set('num_of_block_last_epoch', num_of_block_last_epoch)

        message = get_message(
            last_epoch_number=last_epoch_number,
            num_of_block_last_epoch=num_of_block_last_epoch
        )
        print(message)
        webhook.send(message)
