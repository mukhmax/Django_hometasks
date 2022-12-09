from django.db import models


class Sensor(models.Model):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=100)


class Measurement(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name='measurements')
    temperature = models.DecimalField(decimal_places=1, max_digits=3)
    time = models.DateTimeField(auto_now_add=True)
    picture = models.ImageField(upload_to='pictures/', null=True, blank=True)
