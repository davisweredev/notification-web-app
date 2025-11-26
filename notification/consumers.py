import json
from channels.generic.websocket import AsyncWebsocketConsumer

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
    
        self.user = self.scope["user"]
        
        if self.user.is_anonymous:
            await self.close()
            return

        self.room_group_name = f'notifications_{self.user.id}'
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
       

    async def disconnect(self, close_code):
        if hasattr(self, 'room_group_name'):
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    async def receive(self, text_data):
        pass

    async def send_notification(self, event):
        await self.send(text_data=json.dumps({
            'type': 'notification',
            'message': event['message'],
            'sender': event['sender'],
            'id': event['id'],
        }))

    async def notification_read(self, event):
        await self.send(text_data=json.dumps({
            'type': 'read',
            'id': event['id'],
        }))