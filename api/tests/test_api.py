from django.test import TestCase

from rest_framework.test import APIClient

from api.tests.test_user import ApiUserTest
from api.tests.test_entry import ApiEntryTest
from api.tests.test_device import ApiDeviceTest


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
            'datetime': '12/25/2019T14:00:00Z'
        }
        self.entry_api.post(device_id, entry_data)
        self.entry_api.get(device_id, {}, entry_data)
        device_data = {
            'id': device_id,
            'name': 'new device 1'
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
                'datetime': '12/25/2019T10:00:00Z',
                'satellites': 4,
            },
            {
                'latitude': 51.678123,
                'longitude': 47.563214,
                'datetime': '12/25/2019T10:30:00Z'
            },
            {
                'latitude': 55.547825,
                'longitude': 46.123874,
                'datetime': '12/25/2019T11:00:00Z'
            },
            {
                'latitude': 53.678123,
                'longitude': 43.563214,
                'datetime': '12/26/2019T15:30:00Z',
                'satellites': 3,
            },
            {
                'latitude': 52.346774,
                'longitude': 45.569303,
                'datetime': '12/26/2019T16:00:00Z',
                'satellites': 5,
            },
        ]
        data = {}
        for entry in entries:
            self.entry_api.post(device_id, entry)
            self.entry_api.get(device_id, data, entry)
        self.entry_api.get_by_datetime(device_id, '12/25/2019T10:25:00Z', entries[1:])
        self.entry_api.get_by_datetime(device_id, '12/25/2019T11:05:00Z', entries[3:])
        self.entry_api.get_by_datetime(device_id, '12/25/2019T09:30:00Z', entries)
        self.entry_api.get_by_datetime(device_id, '12/26/2019T08:00:00Z', entries[5:])
        self.entry_api.get_by_datetime(device_id, '12/27/2019T06:00:00Z', [])
        self.user_api.logout()

    def test_unauthorized_case(self):
        self.user_api.register()
        self.user_api.login()
        self.user_api.logout()

        device_id = 'abcdef123456abcd'
        entry_data = {
            'latitude': 12.123456,
            'longitude': 21.123456,
            'datetime': '11/20/2019T10:00:00Z'
        }
        self.entry_api.post_unauthorized(device_id, entry_data)
        self.entry_api.get_unauthorized(device_id, entry_data)

        self.device_api.get_unauthorized({})
        self.device_api.put_unauthorized({})

    def test_formats(self):
        self.user_api.register()
        self.user_api.login()
        device_id = '8765432187654321'
        entries = [
            {
                'latitude': 52.278123,
                'longitude': 47.163214,
                'datetime': '12/15/2019T00:00:00Z'
            },
            {
                'latitude': 51.678123,
                'longitude': 47.563214,
                'datetime': '12/16/2019T14:30:00Z'
            },
        ]
        for entry in entries:
            self.entry_api.post(device_id, entry)
        expected_kml = (
            '<?xml version="1.0" encoding="UTF-8"?>'
            '<kml xmlns="http://www.opengis.net/kml/2.2">'
            '<Document>'
            '<name>entries</name>'
            '<Placemark>'
            '<name>Point #1</name>'
            '<TimeStamp><when>12/15/2019T00:00:00Z</when></TimeStamp>'
            '<Point><coordinates>47.163214,52.278123</coordinates></Point>'
            '</Placemark>'
            '<Placemark>'
            '<name>Point #2</name>'
            '<TimeStamp><when>12/16/2019T14:30:00Z</when></TimeStamp>'
            '<Point><coordinates>47.563214,51.678123</coordinates></Point>'
            '</Placemark>'
            '</Document>'
            '</kml>'
        )
        expected_gpx = (
            '<?xml version="1.0" encoding="UTF-8"?>'
            '<gpx xmlns="http://www.topografix.com/GPX/1/1">'
            '<name>entries</name>'
            '<wpt lat="52.278123" lon="47.163214">'
            '<time>12/15/2019T00:00:00Z</time>'
            '<name>Point #1</name>'
            '</wpt>'
            '<wpt lat="51.678123" lon="47.563214">'
            '<time>12/16/2019T14:30:00Z</time>'
            '<name>Point #2</name>'
            '</wpt>'
            '</gpx>'
        )
        str_datetime = '12/15/2019T00:00:00Z'
        self.entry_api.get_by_type(device_id, 'kml', str_datetime, expected_kml)
        self.entry_api.get_by_type(device_id, 'gpx', str_datetime, expected_gpx)
        self.user_api.logout()

    def test_formats_empty_case(self):
        self.user_api.register()
        self.user_api.login()
        device_id = '8765432187654321'
        expected_kml = (
            '<?xml version="1.0" encoding="UTF-8"?>'
            '<kml xmlns="http://www.opengis.net/kml/2.2">'
            '<Document>'
            '<name>entries</name>'
            '</Document>'
            '</kml>'
        )
        expected_gpx = (
            '<?xml version="1.0" encoding="UTF-8"?>'
            '<gpx xmlns="http://www.topografix.com/GPX/1/1">'
            '<name>entries</name>'
            '</gpx>'
        )
        str_datetime = '01/25/2020T00:00:00Z'
        self.entry_api.get_by_type(device_id, 'kml', str_datetime, expected_kml)
        self.entry_api.get_by_type(device_id, 'gpx', str_datetime, expected_gpx)
        self.user_api.logout()

    def test_nmea_entries(self):
        self.user_api.register()
        self.user_api.login()
        device_id = 'abcdef123456abcd'
        entries = [
            '$GPRMC,125504.049,A,5542.2389,N,03741.6063,E,0.19,25.82,200919,,,*17',
            '$GPRMC,164125,A,4425.8988,N,07543.5370,W,000.0,000.0,151116,,,A*66',
            '$GPRMC,081836,A,3751.65,S,14507.36,E,000.0,360.0,130998,011.3,E*62',
            '$GPRMC,225446,A,4916.45,N,12311.12,W,000.5,054.7,191194,020.3,E*68',
        ]
        for entry in entries:
            self.entry_api.post(device_id, entry, 'nmea')
        expected_entries = [
            {
                'latitude': 55.703982,
                'longitude': 37.693438,
                'datetime': '09/20/2019T12:55:04Z'
            },
            {
                'latitude': 44.431647,
                'longitude': -75.725617,
                'datetime': '11/15/2016T16:41:25Z'
            },
            {
                'latitude': -37.860833,
                'longitude': 145.122667,
                'datetime': '09/13/1998T08:18:36Z'
            },
            {
                'latitude': 49.274167,
                'longitude': -123.185333,
                'datetime': '11/19/1994T22:54:46Z'
            },
        ]
        data = {}
        for expected_entry in expected_entries:
            self.entry_api.get(device_id, data, expected_entry)
        self.user_api.logout()

    def test_nmea_invalid_case(self):
        self.user_api.register()
        self.user_api.login()
        device_id = 'abcdef123456abcd'
        entries = [
            '$GPRMC,,V,,,,,,,080907,9.6,E,N*31',
            '$GPRMC,,V,,,,,,,,,,N*53',
            '$GPRMC,121738.086,V,,,,,0.00,0.00,290316,,,N*42',
        ]
        for entry in entries:
            args = (device_id, entry, 'nmea')
            self.assertRaises(ValueError, self.entry_api.post, *args)
        self.user_api.logout()

    def test_invalid_satellites(self):
        self.user_api.register()
        self.user_api.login()
        device_id = '1234123412341234'
        invalid_satellites = {
            'latitude': 55.678123,
            'longitude': 48.123874,
            'datetime': '12/25/2019T14:00:00Z',
            'satellites': 17,
        }
        self.entry_api.post_invalid_params(device_id, invalid_satellites)
        invalid_satellites['satellites'] = 2
        self.entry_api.post_invalid_params(device_id, invalid_satellites)
        self.user_api.logout()

    def test_invalid_coordinates(self):
        self.user_api.register()
        self.user_api.login()
        device_id = '1234123412341234'
        invalid_latitude = {
            'latitude': 180.000000,
            'longitude': 48.123874,
            'datetime': '12/25/2019T14:00:00Z',
        }
        self.entry_api.post_invalid_params(device_id, invalid_latitude)
        invalid_latitude['latitude'] = -180.000000
        self.entry_api.post_invalid_params(device_id, invalid_latitude)
        invalid_latitude['latitude'] = 55.678123
        invalid_latitude['longitude'] = 181.678123
        self.entry_api.post_invalid_params(device_id, invalid_latitude)
        invalid_latitude['longitude'] = -181.678123
        self.entry_api.post_invalid_params(device_id, invalid_latitude)
        self.user_api.logout()
