from __future__ import unicode_literals
import websockets
import asyncio
import json
from arsmoon.taskapp.celery import app


async def receive_messages(account_name):
    ws_url = 'wss://testnet.bitmex.com/realtime?subscribe=instrument'
    async with websockets.connect(ws_url) as websocket:
        async for message in websocket:
            message_json = json.loads(message)
            if 'action' in message_json and message_json['action'] == 'update' and 'data' in message_json:
                bitmex_data = {}
                for data in message_json['data']:
                    if 'markPrice' in data:
                        bitmex_data['price'] = data['markPrice']
                        bitmex_data['symbol'] = data['symbol']
                        bitmex_data['timestamp'] = data['timestamp']
                        bitmex_data['account'] = account_name
                        print(bitmex_data)


@app.task()
def bitmex_instrument_data(account_name):
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(receive_messages(account_name))
        loop.run_forever()
    finally:
        loop.stop()
        loop.close()
        print('Close loop')  # close websocket Logger can be used
