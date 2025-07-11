"""
Serializers for user management.
"""

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['role'] = user.role
        token['username'] = user.username
        return token

class StaffUserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name', 'role']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate_role(self, value):
        if value != 'staff':
            raise serializers.ValidationError("Only staff users can be created here.")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user