from django.db import models


class Campaign(models.Model):
    name = models.CharField(max_length=25)
    description = models.TextField(max_length=300)
    latitude = models.DecimalField(max_digits=13, decimal_places=9)
    longitude = models.DecimalField(max_digits=13, decimal_places=9)
    picture = models.ImageField(upload_to='pictures/')
    file = models.FileField(upload_to='files/')

    def __str__(self):
        return self.name
