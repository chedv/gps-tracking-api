from rest_framework import renderers


class NmeaRenderer(renderers.BaseRenderer):
    media_type = 'text/nmea'
    format = 'nmea'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        return data.encode(self.charset)
