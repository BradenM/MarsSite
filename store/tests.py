from django.test import TestCase
from .models import Cart, CartEntry
from django.contrib.auth.models import User
from repair.models import Device, Family, Repair, DeviceRepair, PHONE

class CartTest(TestCase):

    def setUp(self):
        # Create two devices, two in family, one not
        self.iphone_x = Device.objects.create(
            name = "iPhone X",
            device_type = PHONE,
            brand = "Apple"
        )

        self.iphone_6 = Device.objects.create(
            name = "iPhone 6",
            has_family = True,
            family_identifier = '6',
        )

        self.iphone_6s = Device.objects.create(
            name = "iPhone 6s",
            has_family = True,
            family_identifier = '6s',
        )

        # iPhone 6 Family
        self.iphone_6_family = Family.objects.create(
            name = "iPhone 6",
            brand = "Apple",
            device_type = PHONE,
            image = 'largeX.png'
        )
        self.iphone_6_family.devices.add(self.iphone_6)
        self.iphone_6_family.devices.add(self.iphone_6s)

        # Three Repairs
        self.screen_repair = Repair.objects.create(name="Screen Repair")
        self.battery_repair = Repair.objects.create(name="Battery Repair")

        # Add a screen repair to iPhone X
        DeviceRepair.objects.create(
            device = self.iphone_x,
            repair = self.screen_repair,
            type = "screen", 
            price = 89.99
        )

        self.order = DeviceRepair.objects.create(
            device = self.iphone_x,
            repair = self.battery_repair,
            type = "battery", 
            price = 19.99
        )

    def test_cart(self):
        print(f"DEVICE REPAIR (PRODUCT):: {self.order}")

        self.cart, created = Cart.objects.get_or_create(user=None)
        print(f"CART CREATED::{self.cart}")

        self.cart_entry = CartEntry.objects.create(product=self.order, cart=self.cart)
        self.second_entry = CartEntry.objects.create(product=self.order, cart=self.cart)

        user_entries = CartEntry.objects.filter(cart=self.cart)
        print(self.cart_entry)
        print(self.cart)
        print(user_entries)