from .admin import (ServiceListCreateView, ServiceDetailView,
                    CategoryListCreateView, CategoryDetailView,
                    BranchListCreateView, BranchDetailView,
                    ServiceCounterListCreateView, ServiceCounterDetailView)
from .dashboard import BranchDashboardView
from .kiosk import TicketCreateView
from .ticket import MyTicketsView, TicketActionView, CounterQueueView

# TODO change all the hardcoded strings to constants or enums (Status, actions, etc.)
