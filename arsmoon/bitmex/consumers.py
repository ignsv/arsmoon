import json
from channels.generic.websocket import AsyncWebsocketConsumer
from arsmoon.bitmex.models import Account, ClientAccountCounter
from arsmoon.bitmex.tasks import bitmex_instrument_data
from arsmoon.taskapp.celery import app
from channels.db import database_sync_to_async


class BitmexConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    @database_sync_to_async
    def get_account(self, name):
        return Account.objects.filter(name=name).first()

    @database_sync_to_async
    def get_client_counter(self, name):
        return ClientAccountCounter.objects.filter(account__name=name).first()

    @database_sync_to_async
    def create_client_counter(self, account, task_id):
        return ClientAccountCounter.objects.create(account=account, count=1, task_id=task_id)

    @database_sync_to_async
    def update_client_counter_number(self, client_account, number):
        client_account.count = client_account.count + number
        return client_account.save()

    @database_sync_to_async
    def delete_client_counter_number(self, client_account):
        return client_account.delete()

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        if 'action' in text_data_json and 'account' in text_data_json:
            account = await self.get_account(name=text_data_json['account'])
            if text_data_json['action'] == 'subscribe':
                if account:
                    await self.channel_layer.group_add(
                        text_data_json['account'],
                        self.channel_name
                    )
                    connector_counter = await self.get_client_counter(text_data_json['account'])
                    if not connector_counter:
                        task_id = bitmex_instrument_data.apply_async(
                            (account.name,)).task_id  # start task to receive data from bitmax
                        await self.create_client_counter(account, task_id=task_id)
                    else:
                        await self.update_client_counter_number(connector_counter, 1)
            elif text_data_json['action'] == 'unsubscribe':
                if account:
                    await self.channel_layer.group_discard(
                        text_data_json['account'],
                        self.channel_name
                    )
                    connector_counter = await self.get_client_counter(text_data_json['account'])
                    if connector_counter:
                        if connector_counter.count == 1:
                            app.control.revoke(connector_counter.task_id, terminate=True) #terminate sending data from bitmex
                            await self.delete_client_counter_number(connector_counter)
                        else:
                            await self.update_client_counter_number(connector_counter, -1)
            else:
                pass
        else:
            result_data_dict = {}
            result_data_dict['message'] = text_data_json
            result_data_dict['type'] = 'bitmex_message'
            await self.channel_layer.group_send(
                text_data_json['account'],
                result_data_dict
            )

    # Receive message from room group
    async def bitmex_message(self, event):
        message = event['message']
        # Send message to WebSocket
        await self.send(text_data=json.dumps(message))
