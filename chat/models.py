from django.db import models
from datetime import datetime


class Room(models.Model):
    name = models.CharField(max_length=1000)

    def __str__(self):
        return self.name

    class Metta:
        verbose_name = "Room"


class Message(models.Model):
    value = models.CharField(max_length=1000000)
    date = models.DateTimeField(default=datetime.now, blank=True)
    user = models.CharField(max_length=20)
    room = models.CharField(max_length=100)

    def __str__(self):
        return self.room

    class Metta:
        verbose_name = "Message"
