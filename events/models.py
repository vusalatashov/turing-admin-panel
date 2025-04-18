from django.db import models
from django.utils import timezone

class Guest(models.Model):
    full_name = models.CharField(max_length=255)
    position_with_company = models.CharField(max_length=255)
    photo_url = models.URLField(blank=True, null=True)  # Contabo URL
    linkedin_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.full_name


class Event(models.Model):
    STATUS_CHOICES = [
        ('UPCOMING', 'Upcoming'),
        ('ONGOING', 'Ongoing'),
        ('PAST', 'Past'),
        ('CANCELLED', 'Cancelled'),
    ]

    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    description = models.TextField()
    event_date = models.DateTimeField()
    register_deadline = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    slots = models.PositiveIntegerField()
    register_link = models.URLField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    photos = models.JSONField(default=list, blank=True)  # list of Contabo URLs
    guests = models.ManyToManyField(Guest, related_name="events")

    def __str__(self):
        return self.name