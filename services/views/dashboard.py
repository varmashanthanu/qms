from datetime import datetime

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsAdmin
from django.utils.timezone import now
from services.models import Branch, Service, Ticket

class BranchDashboardView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request, branch_id):
        try:
            branch = Branch.objects.get(id=branch_id)
        except Branch.DoesNotExist:
            return Response({"error": "Branch not found"}, status=404)

        # 🔍 Parse ?date=YYYY-MM-DD
        date_str = request.query_params.get("date")
        try:
            selected_date = (
                datetime.strptime(date_str, "%Y-%m-%d").date()
                if date_str else now().date()
            )
        except ValueError:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=400)

        # ────────────── COUNTER DATA ──────────────
        counters_data = []
        counters = branch.counters.filter(is_active=True).select_related('assigned_staff')
        for counter in counters:
            current_ticket = Ticket.objects.filter(
                counter=counter,
                status__in=["in_progress", "served"]
            ).order_by('-called_at').first()

            counters_data.append({
                "counter_id": counter.id,
                "counter_name": counter.name,
                "staff": counter.assigned_staff.username if counter.assigned_staff else None,
                "services": [service.name for service in counter.allowed_services.all()],
                "ticket": {
                    "ticket_number": current_ticket.ticket_number,
                    "status": current_ticket.status,
                    "called_at": current_ticket.called_at
                } if current_ticket else None
            })

        # ────────────── SERVICE DATA ──────────────
        services_data = []
        services = branch.services.all()  # Assuming a reverse FK on Service to Branch

        for service in services:
            tickets = Ticket.objects.filter(branch=branch, service=service)
            tickets_on_date = tickets.filter(created_at__date=selected_date)

            services_data.append({
                "service": service.name,
                "pending_count": tickets_on_date.filter(status="pending").count(),
                "in_progress_count": tickets_on_date.filter(status="in_progress").count(),
                "served_count": tickets_on_date.filter(status="served").count(),
            })

        return Response({
            "branch_id": branch.id,
            "branch_name": branch.name,
            "date": selected_date,
            "counters": counters_data,
            "services": services_data,
        })
