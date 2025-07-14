from django.urls import path
from .views import (ServiceListCreateView, ServiceDetailView, CategoryListCreateView, CategoryDetailView,
                    BranchListCreateView, BranchDetailView, ServiceCounterListCreateView, ServiceCounterDetailView,
                    TicketCreateView, MyTicketsView, TicketActionView, BranchDashboardView)

urlpatterns = [
    # Service URLs
    path('services/', ServiceListCreateView.as_view(), name='service-list-create'),
    path('services/<int:pk>/', ServiceDetailView.as_view(), name='service-detail'),

    # Category URLs
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),

    # Branch URLs
    path('branches/', BranchListCreateView.as_view(), name='branch-list-create'),
    path('branches/<int:pk>/', BranchDetailView.as_view(), name='branch-detail'),

    # ServiceCounter URLs
    path('counters/', ServiceCounterListCreateView.as_view(), name='service-counter-list-create'),
    path('counters/<int:pk>/', ServiceCounterDetailView.as_view(), name='service-counter-detail'),

    # Ticket URLs
    path('tickets/', TicketCreateView.as_view(), name='ticket-create'),
    path('my-tickets/', MyTicketsView.as_view(), name='my-tickets'),
    path('tickets/<int:pk>/action/', TicketActionView.as_view(), name='ticket-action'),

    # Dashboard URLs
    path('dashboard/branch/<int:branch_id>/', BranchDashboardView.as_view(), name='branch-dashboard'),

]
