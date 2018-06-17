from django.db import models
from django.contrib.auth.models import User
from billing.models import Order

STATUS_RECEIVED = "Order Received"
STATUS_SHIPPED = "Replacement Shipped"
STATUS_READY = "Ready for Repair"
STATUS_REPAIR = "Repair"
STATUS_PICKUP = "Pickup"
STATUS_COMPLETE = "Complete"

STATUS_CHOICES = (
    (STATUS_RECEIVED, "Order Received."),
    (STATUS_SHIPPED, "Replacement Shipped."),
    (STATUS_READY, "Ready for Repair"),
    (STATUS_REPAIR, "Repair"),
    (STATUS_PICKUP, "Pickup"),
    (STATUS_COMPLETE, "Complete")
)

STATUS_DESC = {
    STATUS_RECEIVED: "Your order has been successfully placed.",
    STATUS_SHIPPED: "Your replacement item is on the way!",
    STATUS_READY: "Your replacement has arrived. See below how to continue.",
    STATUS_REPAIR: "Your device has been received and will be repaired shortly.",
    STATUS_PICKUP: "Your device is fixed and ready for pickup!",
    STATUS_COMPLETE: ""
}


PRIORITY_LOW = 0
PRIORITY_MED = 1
PRIORITY_HIGH = 2

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
    description = models.CharField(
        max_length=256, null=True, blank=True)
    priority = models.IntegerField(
        choices=PRIORITY_CHOICES, default=PRIORITY_LOW)
    date = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        desc = STATUS_DESC[self.status]
        self.description = desc
        super(TrackerUpdate, self).save(*args, **kwargs)

    def __str__(self):
        return f"({self.status} w/ {self.priority} priority) update on {self.date.date()} to ({self.tracker.order})"
