from django.db import models
from django.utils.text import slugify
from django.utils import timezone

from users.models import User

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Define plural name for the model
    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Service(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='services', null=True, blank=True)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

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

class ServiceCounter(models.Model):
    name = models.CharField(max_length=50)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='counters')
    assigned_staff = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'role': 'staff'}
    )
    is_active = models.BooleanField(default=True)
    allowed_services = models.ManyToManyField('Service', blank=True, related_name='counters')

    def __str__(self):
        return f"{self.branch.name} - {self.name}"

class Ticket(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('served', 'Served'),
        ('cancelled', 'Cancelled'),
    ]

    ticket_number = models.CharField(max_length=10)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'role': 'staff'}
    )
    counter = models.ForeignKey(ServiceCounter, on_delete=models.SET_NULL, null=True, blank=True)

    # Optional customer details
    customer_name = models.CharField(max_length=100, blank=True, null=True)
    customer_phone = models.CharField(max_length=20, blank=True, null=True)
    customer_email = models.EmailField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    called_at = models.DateTimeField(null=True, blank=True)
    served_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.ticket_number} ({self.status})"

    def save(self, *args, **kwargs):
        if not self.ticket_number:
            prefix = slugify(self.service.name)[:3].upper()  # e.g. "acc" → "ACC"
            # Count today's tickets for this service
            today = timezone.now().date()
            count_today = Ticket.objects.filter(
                service=self.service,
                branch=self.branch,
                created_at__date=today
            ).count() + 1
            self.ticket_number = f"{prefix}{count_today:03d}"
        super().save(*args, **kwargs)
