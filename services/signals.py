from django.db.models.signals import post_save
from django.dispatch import receiver
from services.models import Ticket
from services.views.ticket import notify_staff_of_new_ticket


@receiver(post_save, sender=Ticket)
def send_ticket_notification(sender, instance, created, **kwargs):
    """
    Signal to notify staff when a new ticket is created.
    """
    if created:
        notify_staff_of_new_ticket(instance)