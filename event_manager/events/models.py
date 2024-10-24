from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils.timezone import timezone, now


class Venue(models.Model):
    name = models.CharField(max_length=100)
    is_virtual = models.BooleanField(default=False)
    address = models.CharField(max_length=200, blank=True, null=True)
    capacity = models.IntegerField(blank=True, null=True)
    virtual_meeting_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name


class Event(models.Model):
    EVENT_STATUS_CHOICES = [
        ('upcoming', 'upcoming'),
        ('ongoing', 'ongoing'),
        ('completed', 'completed')
    ]
    name = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_public = models.BooleanField(default=False)
    location = models.CharField(max_length=100, blank=True, null=True)
    max_participants = models.PositiveIntegerField()
    organizer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='organized_events')
    venue = models.ForeignKey(
        Venue, on_delete=models.CASCADE, related_name='events')
    pub_date = models.TimeField(default=now)
    status = models.CharField(
        max_length=10, choices=EVENT_STATUS_CHOICES, default="upcoming")

    def __str__(self):
        return self.name

    def get_remaining_tickets(self):
        tickets = self.tickets.count()
        return max(0, self.max_participants - tickets)

    def clean(self):
        if self.end_time <= self.start_time:
            raise ValidationError('End time must be after start time.')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def update_status(self):
        now = timezone.now()
        event_start = timezone.make_aware(
            timezone.datetime.combine(self.date, self.start_time))
        event_end = timezone.make_aware(
            timezone.datetime.combine(self.date, self.end_time))

        if now < event_start:
            self.status = 'upcoming'
        elif event_start <= now < event_end:
            self.status = 'ongoing'
        else:
            self.status = 'completed'
        self.save()


class EventReview(models.Model):
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name="reviews")
    reviewer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="event_reviews")
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.event.name} - {self.reviewer.username}"


class Ticket(models.Model):
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name="tickets")
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="tickets")
    price = models.DecimalField(max_digits=8, decimal_places=2)
    purchase_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.event.name} - {self.user.username}"
