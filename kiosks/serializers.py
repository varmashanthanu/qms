from rest_framework import serializers


class KioskKeyExchangeSerializer(serializers.Serializer):
    """
    Serializer for Kiosk Key Exchange.
    """
    kiosk_key = serializers.UUIDField()
