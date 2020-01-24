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
            'datetime': '12/25/2019 14:00:00'
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
        data = {}
        for entry in entries:
            self.entry_api.post(device_id, entry)
            self.entry_api.get(device_id, data, entry)
        self.entry_api.get_by_datetime(device_id, '12/25/2019 10:25:00', entries[1:])
        self.entry_api.get_by_datetime(device_id, '12/25/2019 11:05:00', entries[3:])
        self.entry_api.get_by_datetime(device_id, '12/25/2019 09:30:00', entries)
        self.entry_api.get_by_datetime(device_id, '12/26/2019 08:00:00', entries[5:])
        self.entry_api.get_by_datetime(device_id, '12/27/2019 06:00:00', [])
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

    def test_export(self):
        self.user_api.register()
        self.user_api.login()
        device_id = '8765432187654321'
        entries = [
            {
                'latitude': 52.278123,
                'longitude': 47.163214,
                'datetime': '12/15/2019 00:00:00'
            },
            {
                'latitude': 51.678123,
                'longitude': 47.563214,
                'datetime': '12/16/2019 14:30:00'
            },
        ]
        for entry in entries:
            self.entry_api.post(device_id, entry)
        expected_kml = (
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2">\n'
            '    <Document id="feat_1">\n'
            '        <Placemark id="feat_2">\n'
            '            <name>Point #1</name>\n'
            '            <TimeStamp id="time_0">\n'
            '                <when>12/16/2019 14:30:00</when>\n'
            '            </TimeStamp>\n'
            '            <Point id="geom_0">\n'
            '                <coordinates>51.678123,47.563214,0.0</coordinates>\n'
            '            </Point>\n'
            '        </Placemark>\n'
            '        <Placemark id="feat_3">\n'
            '            <name>Point #2</name>\n'
            '            <TimeStamp id="time_1">\n'
            '                <when>12/15/2019 00:00:00</when>\n'
            '            </TimeStamp>\n'
            '            <Point id="geom_1">\n'
            '                <coordinates>52.278123,47.163214,0.0</coordinates>\n'
            '            </Point>\n'
            '        </Placemark>\n'
            '    </Document>\n'
            '</kml>\n'
        )
        expected_gpx = (
            "<?xml version='1.0' encoding='utf-8'?>\n"
            '<gpx>\n'
            '  <trk>\n'
            '    <name>Point #1</name>\n'
            '    <trkseg>\n'
            '      <trkpt lat="51.678123" lon="47.563214">\n'
            '        <time>12/16/2019 14:30:00</time>\n'
            '      </trkpt>\n'
            '    </trkseg>\n'
            '  </trk>\n'
            '  <trk>\n'
            '    <name>Point #2</name>\n'
            '    <trkseg>\n'
            '      <trkpt lat="52.278123" lon="47.163214">\n'
            '        <time>12/15/2019 00:00:00</time>\n'
            '      </trkpt>\n'
            '    </trkseg>\n'
            '  </trk>\n'
            '</gpx>\n'
        )
        str_datetime = '12/15/2019 00:00:00'
        self.entry_api.get_by_type(device_id, 'kml', str_datetime, expected_kml)
        self.entry_api.get_by_type(device_id, 'gpx', str_datetime, expected_gpx)
        self.user_api.logout()

    def test_nmea_entries(self):
        self.user_api.register()
        self.user_api.login()
        device_id = 'abcdef123456abcd'
        entries = [
            '$GPRMC,125504.049,A,5542.2389,N,03741.6063,E,0.19,25.82,200919,,,*17',
            '$GNRMC,033615.00,A,3157.10477,S,11549.42965,E,0.120,,270115,,,A*73',
            '$GPRMC,164125,A,4425.8988,N,07543.5370,W,000.0,000.0,151116,,,A*66',
        ]
        for entry in entries:
            self.entry_api.post(device_id, entry, 'nmea')
        expected_entries = [
            {
                'latitude': 55.703982,
                'longitude': 37.693438,
                'datetime': '09/20/2019 12:55:04'
            },
            {
                'latitude': -31.951746,
                'longitude': 115.823827,
                'datetime': '01/27/2015 03:36:15'
            },
            {
                'latitude': 44.431647,
                'longitude': -75.725617,
                'datetime': '11/15/2016 16:41:25'
            },
        ]
        data = {}
        for expected_entry in expected_entries:
            self.entry_api.get(device_id, data, expected_entry)
        self.user_api.logout()

    def test_nmea_invalid(self):
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
