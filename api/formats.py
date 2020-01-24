from .gpx import Gpx, GpxTrack, GpxTrackSegment
import simplekml


class KmlFormat:
    def format(self, entries):
        kml = simplekml.Kml()
        for i, entry in enumerate(entries):
            name = 'Point #%d' % (i+1)
            coord = (entry['latitude'], entry['longitude'])
            point = kml.newpoint(name=name, coords=[coord])
            point.timestamp.when = entry['datetime']
        return kml.kml()


class GpxFormat:
    def format(self, entries):
        gpx = Gpx()
        for i, entry in enumerate(entries):
            name = 'Point #%d' % (i+1)
            track = GpxTrack(name=name)
            track_segment = GpxTrackSegment()
            track_segment.point(entry['latitude'], entry['longitude'], entry['datetime'])
            track.segment(track_segment)
            gpx.track(track)
        return gpx.xml()
