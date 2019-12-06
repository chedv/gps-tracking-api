from django.test import TestCase

from api.models import User, Device, Entry
from api.serializers import DeviceSerializer, EntrySerializer
from api.utc_datetime import utc_datetime


class DeviceModelTest(TestCase):
    def setUp(self):
        user = User.objects.create(email="test-example@gmail.com").id
        self.devices = [
            {'id': '1234123412341234', 'name': 'GPS tracker #1', 'owner': user},
            {'id': '1234567812345678', 'name': 'GPS tracker #2', 'owner': user},
            {'id': '8765432187654321', 'name': 'GPS tracker #3', 'owner': user},
            {'id': '8765432112345678', 'name': 'GPS tracker #4', 'owner': user},
        ]
        for device in self.devices:
            serializer = DeviceSerializer(data=device)
            self.assertTrue(serializer.is_valid())
            serializer.save()

    def device_get(self, id, name):
        self.assertEqual(Device.objects.get(id=id).name, name)
        self.assertEqual(Device.objects.get(name=name).id, id)

    def device_delete(self, id):
        device = Device.objects.get(id=id)
        device.delete()

    def device_count(self):
        self.assertEqual(Device.objects.count(), len(self.devices))

    def test_basic(self):
        self.device_count()
        for device in self.devices:
            self.device_get(device['id'], device['name'])
        for device in self.devices:
            self.device_delete(device['id'])
        self.devices = []
        self.device_count()


class EntryModelTest(TestCase):
    def setUp(self):
        user = User.objects.create(email="test-example@gmail.com").id
        device_id = '1234123412341234'
        device_name = 'GPS tracker #1'
        serializer = DeviceSerializer(data={'id': device_id, 'name': device_name, 'owner': user})
        self.assertTrue(serializer.is_valid())
        serializer.save()
        self.entries = [
            {
                'latitude': 52.678123,
                'longitude': 47.563214,
                'datetime': '12/25/2019 10:00:00',
                'device': device_id
            },
            {
                'latitude': 51.678123,
                'longitude': 47.563214,
                'datetime': '12/25/2019 10:30:00',
                'device': device_id
            },
            {
                'latitude': 55.547825,
                'longitude': 46.123874,
                'datetime': '12/25/2019 11:00:00',
                'device': device_id
            },
        ]
        for entry in self.entries:
            serializer = EntrySerializer(data=entry)
            self.assertTrue(serializer.is_valid())
            serializer.save()

    def entry_get(self, entry):
        row = Entry.objects.get(datetime=utc_datetime(entry['datetime']))
        self.assertEqual(row.latitude, entry['latitude'])
        self.assertEqual(row.longitude, entry['longitude'])
        self.assertEqual(row.device_id, entry['device'])

    def entry_count(self):
        self.assertEqual(Entry.objects.count(), len(self.entries))

    def entry_delete(self, str_datetime):
        entry = Entry.objects.get(datetime=utc_datetime(str_datetime))
        entry.delete()

    def test_basic(self):
        self.entry_count()
        for entry in self.entries:
            self.entry_get(entry)
        for entry in self.entries:
            self.entry_delete(entry['datetime'])
        self.entries = []
        self.entry_count()
