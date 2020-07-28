import json
from channels.generic.websocket import AsyncWebsocketConsumer
from arsmoon.bitmex.models import Account, ClientAccountCounter
from arsmoon.bitmex.tasks import bitmex_instrument_data
from arsmoon.taskapp.celery import app


class BitmexConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        if 'action' in text_data_json and 'account' in text_data_json:
            if text_data_json['action'] == 'subscribe':
                account = Account.objects.filter(name=text_data_json['account']).first()
                if account:
                    await self.channel_layer.group_add(
                        text_data_json['account'],
                        self.channel_name
                    )
                    connector_counter = ClientAccountCounter.objects.filter(
                        account__name=text_data_json['account']).first()
                    if not connector_counter:
                        task_id = bitmex_instrument_data.apply_async(
                            (account.name,)).task_id  # start task to receive data from bitmax
                        ClientAccountCounter.objects.create(account=account, count=1, task_id=task_id)
                    else:
                        connector_counter.count = connector_counter.count + 1
                        connector_counter.save()
            elif text_data_json['action'] == 'unsubscribe':
                account = Account.objects.filter(name=text_data_json['account']).first()
                if account:
                    await self.channel_layer.group_discard(
                        text_data_json['account'],
                        self.channel_name
                    )
                    connector_counter = ClientAccountCounter.objects.filter(
                        account__name=text_data_json['account']).first()
                    if connector_counter:
                        if connector_counter.count == 1:
                            app.control.revoke(connector_counter.task_id, terminate=True) #terminate sending data from bitmex
                            connector_counter.delete()
                        else:
                            connector_counter.count = connector_counter.count - 1
                            connector_counter.save()
            else:
                pass
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
