from django.db import models
from django.utils import timezone
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Service, Category, Branch, ServiceCounter, Ticket
from .serializers import (ServiceSerializer, CategorySerializer, BranchSerializer, ServiceCounterSerializer,
                          TicketSerializer, TicketCreateSerializer)
from users.permissions import IsAdmin, IsStaff

# TODO change all the hardcoded strings to constants or enums (Status, actions, etc.)

# --- Service Views ---
class ServiceListCreateView(generics.ListCreateAPIView):
    queryset = Service.objects.all().order_by('-created_at')
    serializer_class = ServiceSerializer
    permission_classes = [IsAdmin]

class ServiceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [IsAdmin]


# --- Category Views ---
class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer
    permission_classes = [IsAdmin]

class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdmin]


# --- Branch Views ---
class BranchListCreateView(generics.ListCreateAPIView):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    permission_classes = [IsAdmin]

class BranchDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    permission_classes = [IsAdmin]


# --- ServiceCounter Views ---
class ServiceCounterListCreateView(generics.ListCreateAPIView):
    queryset = ServiceCounter.objects.all()
    serializer_class = ServiceCounterSerializer
    permission_classes = [IsAdmin]

class ServiceCounterDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ServiceCounter.objects.all()
    serializer_class = ServiceCounterSerializer
    permission_classes = [IsAdmin]


# --- Ticket Views ---
class TicketCreateView(generics.CreateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketCreateSerializer
    permission_classes = []  # Public (no auth) — secure behind device-level controls


# --- Staff Ticket Views ---
class MyTicketsView(generics.ListAPIView):
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated, IsStaff]

    def get_queryset(self):
        user = self.request.user

        # Staff’s active counter(s)
        active_counters = ServiceCounter.objects.filter(
            assigned_staff=user,
            is_active=True
        )

        # Services and branches they are responsible for
        services = Service.objects.filter(counters__in=active_counters).distinct()
        branches = Branch.objects.filter(counters__in=active_counters).distinct()

        return Ticket.objects.filter(
            models.Q(status='in_progress', assigned_to=user) |
            models.Q(
                status='pending',
                assigned_to__isnull=True,
                service__in=services,
                branch__in=branches
            )
        ).distinct().order_by('created_at')

class TicketActionView(APIView):
    permission_classes = [IsAuthenticated, IsStaff]

    def post(self, request, pk):
        user = request.user
        action = request.data.get("action")

        try:
            ticket = Ticket.objects.get(pk=pk)
        except Ticket.DoesNotExist:
            return Response({"error": "Ticket not found"}, status=404)

        # --- CALL ---
        if action == "call":
            if ticket.status != 'pending' or ticket.assigned_to:
                return Response({"error": "Ticket is not available to be called."}, status=400)

            counter = ServiceCounter.objects.filter(assigned_staff=user, is_active=True).first()
            if not counter:
                return Response({"error": "You must be assigned to an active counter."}, status=403)

            ticket.assigned_to = user
            ticket.counter = counter
            ticket.status = 'in_progress'
            ticket.called_at = timezone.now()
            ticket.save()

        # --- SERVE ---
        elif action == "serve":
            if ticket.status != 'in_progress':
                return Response({"error": "Ticket must be in progress to be served."}, status=400)
            if ticket.assigned_to != user:
                return Response({"error": "You are not assigned to this ticket."}, status=403)

            ticket.status = 'served'
            ticket.served_at = timezone.now()
            ticket.save()

        # --- COMPLETE ---
        elif action == "complete":
            if ticket.status != 'served':
                return Response({"error": "Only served tickets can be completed."}, status=400)
            if ticket.assigned_to != user:
                return Response({"error": "You are not assigned to this ticket."}, status=403)

            ticket.status = 'served'  # keep status for historical integrity (or change to 'completed')
            ticket.completed_at = timezone.now()
            ticket.save()

        # --- SKIP ---
        elif action == "skip":
            if ticket.status != 'in_progress':
                return Response({"error": "Only in-progress tickets can be skipped."}, status=400)
            if ticket.assigned_to != user:
                return Response({"error": "You are not assigned to this ticket."}, status=403)

            # Requeue ticket
            ticket.status = 'pending'
            ticket.assigned_to = None
            ticket.counter = None
            ticket.called_at = None
            ticket.save()

        # --- TRANSFER ---
        elif action == "transfer":
            if ticket.status not in ['in_progress', 'served']:
                return Response({"error": "Only in-progress tickets can be transferred."}, status=400)
            if ticket.assigned_to != user:
                return Response({"error": "You are not assigned to this ticket."}, status=403)

            to_counter_id = request.data.get("to_counter")
            if not to_counter_id:
                return Response({"error": "Target counter ID (to_counter) is required."}, status=400)

            try:
                new_counter = ServiceCounter.objects.get(id=to_counter_id, is_active=True)
            except ServiceCounter.DoesNotExist:
                return Response({"error": "Target counter not found or inactive."}, status=404)

            if new_counter.branch != ticket.branch:
                return Response({"error": "Cannot transfer ticket to a counter in a different branch."}, status=400)

            if not new_counter.assigned_staff:
                return Response({"error": "Target counter has no assigned staff."}, status=400)

            # Perform transfer
            ticket.counter = new_counter
            ticket.assigned_to = new_counter.assigned_staff
            ticket.save()

        else:
            return Response({"error": "Invalid action."}, status=400)

        return Response(TicketSerializer(ticket).data, status=200)
