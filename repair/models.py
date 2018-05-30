from django.db import models


class Repair(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField(default=0.00)

    def __str__(self):
        return f"{self.name} - ${self.price}"

class Family(models.Model):
    name = models.CharField(max_length=200)
    brand = models.CharField(max_length=200)
    image = models.ImageField(upload_to="imgs/")

    def __str__(self):
        return self.name

class Device(models.Model):
    name = models.CharField(max_length=200)
    family = models.ForeignKey(Family, on_delete=models.CASCADE, default=None)
    repairs = models.ManyToManyField(Repair)

    def __str__(self):
        return self.name
