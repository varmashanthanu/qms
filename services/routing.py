from django.urls import path
from . import consumers


websocket_urlpatterns = [
    path('ws/staff-dashboard/<int:user_id>/', consumers.StaffDashboardConsumer.as_asgi()),
]