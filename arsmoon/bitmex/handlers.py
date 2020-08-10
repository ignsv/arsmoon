import websockets
import json


class BitmexHandler:
    ws_bitmex_url = 'wss://testnet.bitmex.com/realtime?subscribe=instrument'

    async def handle_bitmex_data(self, account_name, channel_layer):
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
                            await channel_layer.group_send(
                                account_name,
                                {
                                    'type': 'bitmex_message',
                                    'message' : bitmex_data,
                                }
                            )
