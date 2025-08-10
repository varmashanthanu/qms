import json
from channels.generic.websocket import AsyncWebsocketConsumer

class StaffDashboardConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for staff dashboard.
    Handles real-time updates for staff users by user_id.
    """

    async def connect(self):
        """
        Handles new WebSocket connection.
        Adds the user to a group based on their user_id.
        """
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        self.group_name = f'staff_{self.user_id}'

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        """
        Handles WebSocket disconnection.
        Removes the user from their group.
        """
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        """
        Handles messages received from the frontend.
        Currently not implemented.
        """
        pass

    async def send_new_ticket(self, event):
        """
        Sends a new ticket event to the frontend.
        """
        await self.send(text_data=json.dumps({
            "type": "new_ticket",
            "ticket": event["ticket"],
        }))