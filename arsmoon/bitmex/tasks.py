from __future__ import unicode_literals
import asyncio
from arsmoon.taskapp.celery import app
from arsmoon.bitmex.handlers import BitmexHandler


@app.task()
def bitmex_instrument_data(account_name):
    loop = asyncio.get_event_loop()
    try:
        handler = BitmexHandler()
        loop.run_until_complete(handler.receive_messages(account_name))
        loop.run_forever()
    finally:
        loop.stop()
        loop.close()
        print('Close loop')  # close loop. Logger can be used
