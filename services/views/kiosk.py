from rest_framework import generics

from services.models import Ticket
from services.serializers import TicketCreateSerializer

# --- Ticket Views ---
class TicketCreateView(generics.CreateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketCreateSerializer
    permission_classes = []  # Public (no auth) — secure behind device-level controls


