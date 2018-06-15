from django.db import models
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from django.template.defaultfilters import slugify
from django import forms

PHONE = "Phone"
TAB = "Tablet"
LAP = "Laptop"
DEV_TYPES = (
    (PHONE, "Phone"),
    (TAB, "Tablet"),
    (LAP, "Laptop")
)

class Repair(models.Model):
    name = models.CharField(max_length=200)
    desc = models.CharField(max_length=4012, blank=True)
    short_name = models.CharField(max_length=200, blank=True)
    icon = models.CharField(max_length=200, blank=True)
    bulma_icon_color = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.name}"


class DeviceRepair(models.Model):
    device = models.ForeignKey('Device', related_name="repair", on_delete=models.CASCADE)
    repair = models.ForeignKey(Repair, related_name="repair", on_delete=models.CASCADE)
    type = models.CharField(max_length=200, default="screen")
    price = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.repair} - {self.device} - ${self.price}"


class Family(models.Model):
    name = models.CharField(max_length=200)
    brand = models.CharField(max_length=200)
    device_type = models.CharField(max_length=200, choices=DEV_TYPES, default=PHONE)
    image = models.ImageField()
    devices = models.ManyToManyField('Device', related_name="devices")

    def device_names(self):
        name = ""
        for d in self.devices.all():
            if d.name != self.name:
                name += f" {d.family_identifier},"
        name = name.rstrip(',')
        return name

    def format_repairs(self):
        first_device = self.devices.all()[0]
        repair_format = "Available: "
        for r in Repair.objects.filter(repairs=first_device)[:4]:
            repair_format += f" {r.name},"
        repair_format += " and more!"
        return repair_format


    def __str__(self):
        names = self.device_names()
        return f"{self.name} + {names}"

class Device(models.Model):
    name = models.CharField(max_length=200)
    device_type = models.CharField(max_length=200, choices=DEV_TYPES, default=PHONE)
    repairs = models.ManyToManyField(Repair, through='DeviceRepair', related_name="repairs")
    has_family = models.BooleanField(default=False)
    family_identifier = models.CharField(max_length=100, blank=True, null=True)
    brand = models.CharField(max_length=200, blank=True, null=True)
    image = models.ImageField(blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)

    def format_repairs(self):
        repair_format = "Available: "
        for r in Repair.objects.filter(repairs=self)[:4]:
            repair_format += f" {r.name},"
        repair_format += " and more!"
        return repair_format
        
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Device, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
