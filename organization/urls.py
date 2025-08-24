from django.urls import path
from .views import BranchListCreateView, BranchDetailView, BranchDashboardView

urlpatterns = [
    # Branch URLs
    path('branches/', BranchListCreateView.as_view(), name='branch-list-create'),
    path('branches/<int:pk>/', BranchDetailView.as_view(), name='branch-detail'),
    # Dashboard URLs
    path('dashboard/branch/<int:branch_id>/', BranchDashboardView.as_view(), name='branch-dashboard'),

]
