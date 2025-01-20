import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from hashlib import md5
from chat.models import ChatModel


class chatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        my_id = self.scope['user']
        other_id = self.scope['url_route']['kwargs']['username']

        if my_id.is_authenticated:
            combined_ids = ''.join(sorted([str(my_id), str(other_id)]))
            self.room_name = md5(combined_ids.encode()).hexdigest()[:8]
            self.room_group_name = f'chat_{self.room_name}'
            
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

            await self.accept()
            print(self.room_group_name)

    async def disconnect(self, code):
        self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_layer
        )

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        message = data['message']
        username = data['username']
        to = data['to']

        await self.save_message(username,self.room_group_name, message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type':'chat_message',
                'message':message,
                'username':username,
                'to':to
            }
        )

    async def chat_message(self,event):
        message = event['message'],
        username = event['username']
        to=event['to']

        await self.send(text_data=json.dumps({
            'message':message,
            'username':username,
            'to':to
        }))

    @database_sync_to_async
    def save_message(self, username, thread_name, message):
        ChatModel.objects.create(username=username, message=message, thread_name=thread_name)

    
    