from rest_framework import generics
from rest_framework.permissions import AllowAny

from services.models import Ticket
from services.serializers import TicketCreateSerializer
from services.permissions import IsKioskToken

# --- Ticket Views ---
class TicketCreateView(generics.CreateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketCreateSerializer
    permission_classes = [IsKioskToken]
