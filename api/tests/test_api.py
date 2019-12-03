from django.test import TestCase

from rest_framework.test import APIClient

from .test_user import ApiUserTest
from .test_entry import ApiEntryTest
from .test_device import ApiDeviceTest


class ApiTest(TestCase):
    def setUp(self):
        user_data = {
            'email': 'example001@email.com',
            'password': 'example1234example1234'
        }
        self.client = APIClient()
        self.user_api = ApiUserTest(self.client, user_data)
        self.entry_api = ApiEntryTest(self.client)
        self.device_api = ApiDeviceTest(self.client)

    def test_basic(self):
        self.user_api.register()
        self.user_api.login()
        device_id = '1234123412341234'
        entry_data = {
            'latitude': 55.678123,
            'longitude': 48.123874,
            'datetime': '12/25/2019 14:00:00'
        }
        self.entry_api.post(device_id, entry_data)
        self.entry_api.get(device_id, entry_data)
        device_data = {
            'id': device_id,
            'name': 'new device'
        }
        self.device_api.get(device_data)
        new_device_data = {
            'id': device_id,
            'name': 'GPS tracker #1'
        }
        self.device_api.put(new_device_data)
        self.device_api.get(new_device_data)
        self.user_api.logout()

    def test_advanced(self):
        self.user_api.register()
        self.user_api.login()
        device_id = '1234123412341234'
        entries = [
            {
                'latitude': 52.678123,
                'longitude': 47.563214,
                'datetime': '12/25/2019 10:00:00'
            },
            {
                'latitude': 51.678123,
                'longitude': 47.563214,
                'datetime': '12/25/2019 10:30:00'
            },
            {
                'latitude': 55.547825,
                'longitude': 46.123874,
                'datetime': '12/25/2019 11:00:00'
            },
            {
                'latitude': 53.678123,
                'longitude': 43.563214,
                'datetime': '12/26/2019 15:30:00'
            },
            {
                'latitude': 52.346774,
                'longitude': 45.569303,
                'datetime': '12/26/2019 16:00:00'
            },
        ]
        for entry in entries:
            self.entry_api.post(device_id, entry)
            self.entry_api.get(device_id, entry)
        self.entry_api.get_by_datetime(device_id, entries[1:], '12/25/2019 10:25:00')
        self.entry_api.get_by_datetime(device_id, entries[3:], '12/25/2019 11:05:00')
        self.entry_api.get_by_datetime(device_id, entries, '12/25/2019 09:30:00')
        self.entry_api.get_by_datetime(device_id, entries[5:], '12/26/2019 08:00:00')
        self.entry_api.get_by_datetime(device_id, [], '12/27/2019 06:00:00')
        self.user_api.logout()

    def test_unauthorized(self):
        self.user_api.register()
        self.user_api.login()
        self.user_api.logout()

        device_id = 'abcdef123456abcd'
        entry_data = {
            'latitude': 12.123456,
            'longitude': 21.123456,
            'datetime': '11/20/2019 10:00:00'
        }
        self.entry_api.post_unauthorized(device_id, entry_data)
        self.entry_api.get_unauthorized(device_id, entry_data)

        self.device_api.get_unauthorized({})
        self.device_api.put_unauthorized({})
