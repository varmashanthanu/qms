from django.db import models
from django.utils import timezone
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from services.models import Service, Branch, ServiceCounter, Ticket
from services.serializers import TicketSerializer
from users.permissions import IsStaff

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

class CounterQueueView(APIView):
    permission_classes = [IsAuthenticated, IsStaff]

    def get(self, request, pk):
        user = request.user

        try:
            counter = ServiceCounter.objects.get(id=pk, is_active=True)
        except ServiceCounter.DoesNotExist:
            return Response({"error": "Counter not found or inactive"}, status=404)

        if counter.assigned_staff != user:
            return Response({"error": "You are not assigned to this counter."}, status=403)

        allowed_services = counter.allowed_services.all()

        limit_param = request.query_params.get("limit", 5)
        try:
            limit = min(int(limit_param), 20)
        except ValueError:
            return Response({"error": "Invalid limit. Must be an integer."}, status=400)

        current_ticket = Ticket.objects.filter(
            counter=counter,
            status__in=["in_progress", "served"]
        ).order_by('-called_at').first()

        pending_tickets = Ticket.objects.filter(
            branch=counter.branch,
            service__in=allowed_services,
            status='pending'
        ).order_by('created_at')[:limit]

        return Response({
            "counter_id": counter.id,
            "staff": user.username,
            "services": [s.name for s in allowed_services],
            "current_ticket": {
                "ticket_number": current_ticket.ticket_number,
                "status": current_ticket.status,
                "called_at": current_ticket.called_at,
                "customer_name": current_ticket.customer_name
            } if current_ticket else None,
            "next_pending": [
                {
                    "ticket_number": t.ticket_number,
                    "created_at": t.created_at,
                    "customer_name": t.customer_name
                } for t in pending_tickets
            ]
        })
