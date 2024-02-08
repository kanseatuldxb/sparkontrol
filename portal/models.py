from django.db import models
from django.contrib.auth.models import User
from auditlog.registry import auditlog
from datetime import datetime
import uuid


class Location(models.Model):
    serial_number = models.CharField(max_length=100,editable=True,)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    # Add other fields as needed

    def __str__(self):
        return self.name

class Remote(models.Model):
    name = models.CharField(max_length=100)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    serial_number = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    manufacturer = models.CharField(max_length=100,default="SparkControl")
    # Add other fields as needed

    def __str__(self):
        return self.name

class Incident(models.Model):
    remote = models.ForeignKey(Remote, on_delete=models.CASCADE)
    event_type = models.CharField(max_length=100)
    call = models.DateTimeField(blank=True, null=True)
    acknowledge = models.DateTimeField(blank=True, null=True)
    reset = models.DateTimeField(blank=True, null=True) #123

    timestamp = models.DateTimeField(auto_now_add=True)
    # Add other fields as needed

    def __str__(self):
        return f"{self.remote.name} - {self.timestamp} - {self.event_type}"
    
class Subscription(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    subscriber = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    # Add other fields as needed

    def __str__(self):
        return f"{self.location.name} - {self.subscriber.username}"
    
auditlog.register(Location)
auditlog.register(Remote)
auditlog.register(Incident)
auditlog.register(Subscription)


