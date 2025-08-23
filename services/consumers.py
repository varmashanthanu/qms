import json
import logging

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from typing import Coroutine, List

from services.models import ServiceCounter


@database_sync_to_async
def get_user_services(user_id: int) -> List[int]:
    """
    Channels cannot perform synchronous database calls using Django ORM. This sync to async method will take care
    of ORM calls in the async operations
    Args:
        user_id: ID of the user to get the allowed services for

    Returns:
        list of service IDs
    """
    # Each counter has a set of allowed services. Each counter is assigned to a staff user
    service_counters = ServiceCounter.objects.filter(assigned_staff__id=user_id)
    if not service_counters:
        return []

    services_list = []
    for service_counter in service_counters:
        services = service_counter.allowed_services.all()
        if services:
            services_list.extend([service.id for service in services])

    return services_list


class StaffDashboardConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for staff dashboard.
    Handles real-time updates for staff users by user_id.
    """
    user_id = None
    group_names = []

    async def connect(self) -> None:
        """
        Staff dashboard channel will connect to 2 groups:
            1. All notifications for the specific staff user
            2. Notifications for each service the staff user is assigned to
        """
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        self.group_names = [f'staff_{self.user_id}']  # This is the base group for user specific notifications

        # We also want to add Service specific groups as needed
        # Fetch services asynchronously
        service_ids = await get_user_services(user_id=self.user_id)
        for service_id in service_ids:
            self.group_names.append(f"service_{service_id}")

        for group_name in self.group_names:
            await self.channel_layer.group_add(
                group_name,
                self.channel_name
            )

        await self.accept()

    async def disconnect(self, close_code) -> None:
        """
        Disconnect from all groups
        Args:
            close_code:

        Returns:

        """
        for group_name in self.group_names:
            await self.channel_layer.group_discard(
                group_name,
                self.channel_name
            )

    async def receive(self, text_data) -> None:
        """
        Receive message from WebSocket.
        Args:
            text_data:

        Returns:

        """
        pass

    async def send_new_ticket(self, event) -> None:
        """
        Sends a new ticket event to the frontend.
        """
        await self.send(text_data=json.dumps({
            "type": "new_ticket",
            "ticket": event["ticket"],
        }))
