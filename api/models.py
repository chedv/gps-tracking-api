from .user import User
from django.db import models


class Device(models.Model):
    id = models.CharField(max_length=16, primary_key=True)
    name = models.CharField(max_length=32, unique=True)
    added = models.DateTimeField(auto_now_add=True, db_index=True)
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Entry(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    datetime = models.DateTimeField(db_index=True)
    satellites = models.PositiveSmallIntegerField(null=True)
    device = models.ForeignKey(to=Device, on_delete=models.CASCADE)

    def get_str_date(self):
        return self.datetime.strftime('%d/%m/%Y')

    def get_str_time(self):
        return self.datetime.strftime('%H:%M:%S')

    def __str__(self):
        to_format = 'latitude: {:f} longitude: {:f} {} {}'
        return to_format.format(self.latitude, self.longitude,
                                self.get_str_date(), self.get_str_time())
