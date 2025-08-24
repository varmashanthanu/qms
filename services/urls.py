from django.urls import path
from .views import (ServiceListCreateView, ServiceDetailView, CategoryListCreateView, CategoryDetailView,
                    ServiceCounterListCreateView, ServiceCounterDetailView,
                    TicketCreateView, MyTicketsView, TicketActionView, CounterQueueView)

urlpatterns = [
    # Service URLs
    path('services/', ServiceListCreateView.as_view(), name='service-list-create'),
    path('services/<int:pk>/', ServiceDetailView.as_view(), name='service-detail'),

    # Category URLs
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),

    # ServiceCounter URLs
    path('counters/', ServiceCounterListCreateView.as_view(), name='service-counter-list-create'),
    path('counters/<int:pk>/', ServiceCounterDetailView.as_view(), name='service-counter-detail'),

    # Ticket URLs
    path('tickets/', TicketCreateView.as_view(), name='ticket-create'),
    path('my-tickets/', MyTicketsView.as_view(), name='my-tickets'),
    path('tickets/<int:pk>/action/', TicketActionView.as_view(), name='ticket-action'),

    # Counter Queue URLs
    path('counters/<int:pk>/queue/', CounterQueueView.as_view(), name='counter-queue'),
]
