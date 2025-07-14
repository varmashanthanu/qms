from rest_framework import serializers
from .models import Service, Category, Branch, ServiceCounter, Ticket

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'name', 'description', 'category', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = ['id', 'name', 'address', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']


class ServiceCounterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCounter
        fields = ['id', 'name', 'branch', 'assigned_staff', 'is_active', 'allowed_services']
        read_only_fields = ['id']


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = [
            'id', 'ticket_number', 'service', 'branch', 'status',
            'assigned_to', 'counter',
            'customer_name', 'customer_phone', 'customer_email',
            'created_at', 'called_at', 'served_at', 'completed_at',
        ]
        read_only_fields = ['id', 'created_at', 'called_at', 'served_at', 'completed_at']

class TicketCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = [
            'id', 'ticket_number', 'service', 'branch', 'status',
            'customer_name', 'customer_phone', 'customer_email',
            'created_at'
        ]
        read_only_fields = ['id', 'ticket_number', 'status', 'created_at']

    def validate(self, data):
        service = data.get('service')
        branch = data.get('branch')

        if not service.is_active:
            raise serializers.ValidationError("Selected service is not active.")

        if not branch.is_active:
            raise serializers.ValidationError("Selected branch is not active.")

        return data
