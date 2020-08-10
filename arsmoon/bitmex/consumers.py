import json
from channels.generic.websocket import AsyncWebsocketConsumer

from arsmoon.bitmex.handlers import BitmexHandler
from arsmoon.bitmex.models import Account, ClientAccountCounter
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
    def create_client_counter(self, account):
        return ClientAccountCounter.objects.create(account=account, count=1)

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
                        account.name,
                        self.channel_name
                    )
                    connector_counter = await self.get_client_counter(text_data_json['account'])
                    if not connector_counter:
                        handler = BitmexHandler()
                        await self.create_client_counter(account)
                        await handler.handle_bitmex_data(account.name, self.channel_layer)
                    else:
                        await self.update_client_counter_number(connector_counter, 1)
            elif text_data_json['action'] == 'unsubscribe':
                if account:
                    await self.channel_layer.group_discard(
                        account.name,
                        self.channel_name
                    )
                    connector_counter = await self.get_client_counter(text_data_json['account'])
                    if connector_counter:
                        if connector_counter.count == 1:
                            await self.delete_client_counter_number(connector_counter)
                        else:
                            await self.update_client_counter_number(connector_counter, -1)
            else:
                pass


    # Receive message from group
    async def bitmex_message(self, event):
        message = event['message']
        # Send message to WebSocket
        await self.send(text_data=json.dumps(message))
