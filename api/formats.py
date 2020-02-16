from xml.dom.minidom import Document
from abc import ABC, abstractmethod


class BaseXmlFormat(ABC):
    def __init__(self, root, **kwargs):
        self.xml = Document()
        self.root = self.xml.createElement(root)
        for key, value in kwargs.items():
            self.root.setAttribute(key, value)
        self.xml.appendChild(self.root)

    @abstractmethod
    def create_point(self, name, lat, lon, datetime):
        pass

    def to_string(self, pretty=False):
        if not pretty:
            return self.xml.toxml(encoding='UTF-8').decode('UTF-8')
        return self.xml.toprettyxml(encoding='UTF-8', indent='    ').decode('UTF-8')


class KmlFormat(BaseXmlFormat):
    def __init__(self):
        super().__init__('kml', xmlns='http://www.opengis.net/kml/2.2')
        self.points = self.xml.createElement('Document')
        name_elem = self.xml.createElement('name')
        name_text = self.xml.createTextNode('entries')

        name_elem.appendChild(name_text)
        self.points.appendChild(name_elem)
        self.root.appendChild(self.points)

    def create_point(self, name, lat, lon, datetime):
        placemark_elem = self.xml.createElement('Placemark')

        placemark_name = self.xml.createElement('name')
        placemark_name_text = self.xml.createTextNode(name)
        placemark_name.appendChild(placemark_name_text)

        timestamp_elem = self.xml.createElement('TimeStamp')
        when_elem = self.xml.createElement('when')
        when_text = self.xml.createTextNode(datetime)
        when_elem.appendChild(when_text)
        timestamp_elem.appendChild(when_elem)

        point_elem = self.xml.createElement('Point')
        coord_elem = self.xml.createElement('coordinates')
        coord_text = self.xml.createTextNode(f'{lon},{lat}')
        coord_elem.appendChild(coord_text)
        point_elem.appendChild(coord_elem)

        placemark_elem.appendChild(placemark_name)
        placemark_elem.appendChild(timestamp_elem)
        placemark_elem.appendChild(point_elem)
        self.points.appendChild(placemark_elem)


class GpxFormat(BaseXmlFormat):
    def __init__(self):
        super().__init__('gpx', xmlns='http://www.topografix.com/GPX/1/1')
        track_name = self.xml.createElement('name')
        track_name_text = self.xml.createTextNode('entries')

        track_name.appendChild(track_name_text)
        self.root.appendChild(track_name)

    def create_point(self, name, lat, lon, datetime):
        point_elem = self.xml.createElement('wpt')

        datetime_elem = self.xml.createElement('time')
        datetime_text = self.xml.createTextNode(datetime)
        datetime_elem.appendChild(datetime_text)

        point_name_elem = self.xml.createElement('name')
        point_name_text = self.xml.createTextNode(name)
        point_name_elem.appendChild(point_name_text)

        point_elem.appendChild(datetime_elem)
        point_elem.appendChild(point_name_elem)
        point_elem.setAttribute('lat', str(lat))
        point_elem.setAttribute('lon', str(lon))
        self.root.appendChild(point_elem)
