from datetime import timedelta

# Create your views here.
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from kiosks.authentication import KioskCompatibleJWTAuthentication
from .models import KioskKey
from .serializers import KioskKeyExchangeSerializer


class KioskTokenExchangeView(APIView):
    """
    View to handle kiosk token exchange.
    """
    authentication_classes = []  # No auth required
    permission_classes = [AllowAny]  # Explicitly allow any user

    @swagger_auto_schema(
        operation_description="Exchange a kiosk key for an access token.",
        request_body=KioskKeyExchangeSerializer,
        responses={
            200: openapi.Response(
                description="Access token for the kiosk.",
                examples={
                    "application/json": {
                        "access_token": "string"
                    }
                }
            ),
            400: "Invalid request data.",
            404: "Kiosk key not found."
        }
    )
    def post(self, request):
        serializer = KioskKeyExchangeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        key = serializer.validated_data['kiosk_key']

        try:
            kiosk_key = KioskKey.objects.get(key=key, used=False)
            if not kiosk_key.is_valid():
                return Response({"detail": "Kiosk key is expired."}, status=status.HTTP_400_BAD_REQUEST)

            # Mark the key as used
            kiosk_key.used = True
            kiosk_key.save()

            # Generate a new access token for the kiosk
            access_token = AccessToken()  # No user, just a kiosk token
            access_token.set_exp(lifetime=timedelta(days=1))  # Set a 1-day expiration
            access_token["scope"] = "kiosk"
            access_token["branch_id"] = str(kiosk_key.branch.id)

            return Response({"access_token": str(access_token), "branch_id": kiosk_key.branch_id},
                            status=status.HTTP_200_OK)
        except KioskKey.DoesNotExist:
            return Response({"detail": "Kiosk key not found or already used."}, status=status.HTTP_404_NOT_FOUND)
