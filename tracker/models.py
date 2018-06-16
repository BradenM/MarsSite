from django.db import models
from django.contrib.auth.models import User
from billing.models import Order

STATUS_RECEIVED = "Order Received"
STATUS_SHIPPED = "Replacement part has shipped"
PRIORITY_LOW = 0
PRIORITY_MED = 1
PRIORITY_HIGH = 2

STATUS_CHOICES = (
    (STATUS_RECEIVED, "Order Received."),
    (STATUS_SHIPPED, "Replacement part has shipped.")
)

PRIORITY_CHOICES = (
    (PRIORITY_LOW, 0),
    (PRIORITY_MED, 1),
    (PRIORITY_HIGH, 2)
)


class Tracker(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(
        Order, related_name='order', on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now=True)
    notes = models.CharField(max_length=256)

    def __str__(self):
        return f"Tracker for {self.order}"


class TrackerUpdate(models.Model):
    tracker = models.ForeignKey(
        Tracker, related_name='updates', on_delete=models.CASCADE)
    status = models.CharField(
        max_length=256, choices=STATUS_CHOICES, default=STATUS_RECEIVED)
    priority = models.IntegerField(
        choices=PRIORITY_CHOICES, default=PRIORITY_LOW)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"({self.status} w/ {self.priority} priority) update on {self.date.date()} to ({self.tracker.order})"
