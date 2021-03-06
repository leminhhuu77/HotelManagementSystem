from django.db import models
from django.utils import timezone

from accounts.models import Guest
# Create your models here.


class Room(models.Model):
    ROOM_TYPES = (
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
    )

    number = models.IntegerField(primary_key=True)
    capacity = models.SmallIntegerField()
    numberOfBeds = models.SmallIntegerField()
    roomType = models.CharField(max_length=20, choices=ROOM_TYPES)

    price = models.FloatField() 
    statusStartDate = models.DateField(null=True)
    statusEndDate = models.DateField(null=True)

    def __str__(self):
        return str(self.number)


class Booking(models.Model):
    roomNumber = models.ForeignKey(Room, on_delete=models.CASCADE)
    guest = models.ForeignKey(Guest, null=True, on_delete=models.CASCADE)
    dateOfReservation = models.DateField(default=timezone.now)
    startDate = models.DateField()
    endDate = models.DateField()

    def __str__(self):
        return str(self.roomNumber) + " " + str(self.guest)

class Bills(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE)
    startDate = models.DateField()
    endDate = models.DateField()
    #booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    totalAmount = models.FloatField()
    summary = models.TextField(null=True)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.guest) + " " + str(self.totalAmount) + "$"