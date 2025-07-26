from django.urls import path
from .views import KioskTokenExchangeView


urlpatterns = [
    path('token/', KioskTokenExchangeView.as_view(), name='kiosk-token-exchange'),
]