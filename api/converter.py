
class Converter:
    def __init__(self, xml_format):
        self.xml = xml_format

    def convert(self, entries):
        xml = self.xml()
        for i, entry in enumerate(entries):
            xml.create_point(lat=entry['latitude'], lon=entry['longitude'],
                             name=f'Point #{i+1}', datetime=entry['datetime'])
        return xml.to_string(pretty=False)
