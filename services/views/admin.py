from rest_framework import generics

from services.models import Service, Category, Branch, ServiceCounter
from services.serializers import (ServiceSerializer, CategorySerializer, BranchSerializer, ServiceCounterSerializer)
from users.permissions import IsAdmin, IsStaff
from rest_framework.permissions import AllowAny

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
    queryset = ServiceCounter.objects.prefetch_related('allowed_services').all()
    serializer_class = ServiceCounterSerializer

    def get_permissions(self):
        # Allow staff to view details, but only admin can update/delete
        if self.request.method in ['GET']:
            return [IsStaff()]
        return [IsAdmin()]

class ServiceCounterDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ServiceCounter.objects.all()
    serializer_class = ServiceCounterSerializer

    def get_permissions(self):
        # Allow staff to view details, but only admin can update/delete
        if self.request.method in ['GET']:
            return [IsStaff()]
        return [IsAdmin()]
