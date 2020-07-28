import websockets
import json


class BitmexHandler:

    async def receive_messages(self, account_name):
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
