from django.db import models

# Create your models here.
class Branch(models.Model):
    name = models.CharField(max_length=100, unique=True)
    address = models.TextField(blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Define plural name for the model
    class Meta:
        verbose_name_plural = "Branches"

    def __str__(self):
        return self.name
