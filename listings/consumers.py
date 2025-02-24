import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Message
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Reject connection if the user is not authenticated
        if self.scope["user"].is_anonymous:
            await self.close()
            return

        self.user = self.scope["user"]
        try:
            # Ensure the receiver_id from the URL is a valid integer
            self.receiver_id = int(self.scope["url_route"]["kwargs"]["receiver_id"])
        except (ValueError, TypeError):
            await self.close()
            return

        # Optionally, verify that the receiver exists in the database
        receiver_exists = await self.user_exists(self.receiver_id)
        if not receiver_exists:
            await self.close()
            return

        # Create a room name based on both user IDs in a consistent order
        self.room_group_name = (
            f"chat_{min(self.user.id, self.receiver_id)}_{max(self.user.id, self.receiver_id)}"
        )

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, "room_group_name"):
            await self.channel_layer.group_discard(self.room_group_name, self.channel_name)


    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({"error": "Invalid JSON format"}))
            return

        message = data.get("message")
        if not message:
            await self.send(text_data=json.dumps({"error": "Message content is required"}))
            return

        # Save the message to the database
        saved_message = await self.save_message(self.user.id, self.receiver_id, message)
        
        # Prepare event payload with optional metadata
        event = {
            "type": "chat_message",
            "message": message,
            "sender_id": self.user.id,
            "message_id": saved_message.id if saved_message else None,
            "timestamp": str(saved_message.created_at) if saved_message else "",
        }
        
        # Broadcast the message to the group
        await self.channel_layer.group_send(self.room_group_name, event)

    async def chat_message(self, event):
        # Relay the event payload to the WebSocket
        await self.send(text_data=json.dumps(event))

    @database_sync_to_async
    def save_message(self, sender_id, receiver_id, content):
        # Create and return the Message instance
        try:
            return Message.objects.create(sender_id=sender_id, receiver_id=receiver_id, content=content)
        except Exception:
            return None

    @database_sync_to_async
    def user_exists(self, user_id):
        return User.objects.filter(id=user_id).exists()
