from django.test import TestCase
from .models import Device, Family, Repair, RepairCost, PHONE

class DeviceTest(TestCase):

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
        RepairCost.objects.create(
            device = self.iphone_x,
            repair = self.screen_repair,
            type = "screen", 
            price = 89.99
        )

        RepairCost.objects.create(
            device = self.iphone_x,
            repair = self.battery_repair,
            type = "battery", 
            price = 19.99
        )


    def test_family(self):
        # What Devices are in the iPhone 6 family?
        family_6 = self.iphone_6_family.devices.all()
        self.assertEqual(list(family_6), [self.iphone_6, self.iphone_6s])
        print(family_6)

    def test_repairs(self):
        # What Repairs does the iphone X have?
        iphone_x_repairs = Repair.objects.filter(repairs=self.iphone_x)
        print('REPAIR TEST: ')
        print(iphone_x_repairs)
        self.assertEqual(list(iphone_x_repairs), [self.screen_repair, self.battery_repair])

    def test_screen_repair(self):
        # Is the iPhone X Screen repair 89.99?
        iphone_x_screenrepair = RepairCost.objects.get(repair=self.screen_repair, device=self.iphone_x)
        print("REPAIR PRICE TEST:")
        print(iphone_x_screenrepair.price)
        self.assertEqual(iphone_x_screenrepair.price, 89.99)
