import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # Kanal guruhiga ulanish
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Kanal guruhidan ajralish
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def send_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json['username']

        # Guruhga xabar yuborish
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'send_message',
                'message': message,
                'username': username,
            }
        )
