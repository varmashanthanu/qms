from rest_framework_simplejwt.authentication import JWTAuthentication

class KioskCompatibleJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        if validated_token.get("scope") == "kiosk":
            # If Kiosk type token, no user is associated
            return None

        # For non kiosk tokens, use the default behavior
        return super().get_user(validated_token)
