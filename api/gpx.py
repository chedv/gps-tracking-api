from lxml import etree


class Gpx:
    def __init__(self):
        self.root = etree.Element('gpx')

    def track(self, track):
        self.root.append(track.root)

    def xml(self, pretty=True):
        raw = etree.tostring(self.root, xml_declaration=True,
                             encoding='utf-8', pretty_print=pretty)
        return raw.decode('utf-8')


class GpxTrack:
    def __init__(self, name):
        self.root = etree.Element('trk')
        name_elem = etree.Element('name')
        name_elem.text = name
        self.root.append(name_elem)

    def segment(self, segment):
        self.root.append(segment.root)


class GpxTrackSegment:
    def __init__(self):
        self.root = etree.Element('trkseg')

    def point(self, lat, lon, time):
        point = etree.Element('trkpt')
        point.set('lat', str(lat))
        point.set('lon', str(lon))
        time_elem = etree.Element('time')
        time_elem.text = time
        point.append(time_elem)
        self.root.append(point)
