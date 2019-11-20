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
