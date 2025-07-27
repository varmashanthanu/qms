from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    ADMIN = 'admin'
    STAFF = 'staff'

    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (STAFF, 'Staff'),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    branch = models.ForeignKey(
        'services.Branch',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='users'
    )

    def __str__(self):
        return f"{self.username} ({self.role})"

    def is_branch_admin(self, branch_id: int) -> bool:
        """
        Check if the user is a branch admin for the given branch ID.
        """
        return self.role == self.ADMIN and self.branch_id == branch_id
