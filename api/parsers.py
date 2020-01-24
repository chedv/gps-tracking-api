from rest_framework import parsers
from datetime import datetime
import pynmea2


class NmeaParser(parsers.BaseParser):
    media_type = 'text/nmea'

    def _get_datetime_object(self, parsed_nmea):
        try:
            datetime_object = datetime.combine(parsed_nmea.datestamp,
                                               parsed_nmea.timestamp)
        except AttributeError:
            datetime_object = datetime.now()
        return datetime_object.replace(microsecond=0)

    def parse(self, stream, media_type=None, parser_context=None):
        nmea = stream.read().decode()
        parsed_nmea = pynmea2.parse(nmea)
        if len(parsed_nmea.lat) == 0 or len(parsed_nmea.lon) == 0:
            raise ValueError('Invalid latitude or longitude values')
        return dict(latitude=round(parsed_nmea.latitude, 6),
                    longitude=round(parsed_nmea.longitude, 6),
                    datetime=self._get_datetime_object(parsed_nmea))
