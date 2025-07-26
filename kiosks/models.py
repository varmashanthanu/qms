from django.db import models

# Create your models here.
import uuid
from datetime import timedelta

from django.db import models
from django.utils import timezone
from services.models import Branch

class KioskKey(models.Model):
    """
    Model to store kiosk keys for secure access.
    """
    key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='kiosk_keys')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    used = models.BooleanField(default=False)

    def __str__(self):
        return f"Kiosk Key {self.key} for Branch {self.branch.name}"

    class Meta:
        verbose_name_plural = "Kiosk Keys"

    def is_valid(self) -> bool:
        """
        Check if the kiosk key is valid (not used and not expired).
        """
        return not self.used and (timezone.now() - self.created_at) <= timedelta(minutes=10)
