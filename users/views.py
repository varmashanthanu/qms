"""
Users app views.
"""

# Create your views here.
from rest_framework import generics
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import CustomTokenObtainPairSerializer, StaffUserCreateSerializer
from .models import User
from .permissions import IsAdmin


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class StaffUserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = StaffUserCreateSerializer
    permission_classes = [IsAdmin]