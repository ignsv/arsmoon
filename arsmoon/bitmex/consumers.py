import json
from channels.generic.websocket import AsyncWebsocketConsumer


class BitmexConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # increase number of connection by one
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        if 'action' in text_data_json and 'account' in text_data_json:
            if text_data_json['action'] == 'subscribe':
                await self.channel_layer.group_add(
                    text_data_json['account'],
                    self.channel_name
                )
            elif text_data_json['action'] == 'unsubscribe':
                await self.channel_layer.group_discard(
                    text_data_json['account'],
                    self.channel_name
                )
                # decrease number of connection by one
            elif 'account' in text_data_json:
                result_data_dict = {}
                result_data_dict['message'] = text_data_json
                result_data_dict['type'] = 'bitmex_message'
                await self.channel_layer.group_send(
                    text_data_json['account'],
                    result_data_dict
                )
            else:
                pass

    # Receive message from room group
    async def bitmex_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps(message))
