import websockets
import json


class BitmexHandler:
    ws_bitmex_url = 'wss://testnet.bitmex.com/realtime?subscribe=instrument'
    ws_server_url = 'ws://localhost:8000/ws/bitmex/'

    async def handle_bitmex_data(self, account_name):

        async with websockets.connect(self.ws_bitmex_url) as websocket:
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
                            # print(bitmex_data)
                            async with websockets.connect(self.ws_server_url) as server_ws:
                                serialized_data = json.dumps(bitmex_data)
                                await server_ws.send(serialized_data)
