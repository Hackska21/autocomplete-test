from django.db import models


class Cities(models.Model):
    name = models.CharField(max_length=255)
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    long = models.DecimalField(max_digits=9, decimal_places=6)
