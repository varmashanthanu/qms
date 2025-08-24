from .admin import (ServiceListCreateView, ServiceDetailView,
                    CategoryListCreateView, CategoryDetailView,
                    ServiceCounterListCreateView, ServiceCounterDetailView)
from organization.views import BranchListCreateView, BranchDetailView
from .kiosk import TicketCreateView
from .ticket import MyTicketsView, TicketActionView, CounterQueueView

# TODO change all the hardcoded strings to constants or enums (Status, actions, etc.)
