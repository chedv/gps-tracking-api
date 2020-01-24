from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_404_NOT_FOUND
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.renderers import JSONRenderer, MultiPartRenderer

from api.models import Device
from api.serializers import DeviceSerializer
from api.services import DeviceService, EntryService
from api.formats import KmlFormat, GpxFormat
from api.parsers import NmeaParser


class DevicesView(APIView):
    def get(self, request):
        devices = Device.objects.filter(owner=request.user).order_by('-added')
        serializer = DeviceSerializer(instance=devices, many=True)
        return Response({'devices': serializer.data})

    def put(self, request):
        query_set = Device.objects.filter(id=request.data.get('id'))
        query_set.update(name=request.data.get('name'))
        return Response(status=HTTP_200_OK)


class EntriesView(APIView):
    parser_classes = (JSONParser, MultiPartParser, NmeaParser)
    renderer_classes = (JSONRenderer, MultiPartRenderer)

    formats = dict(kml=KmlFormat(), gpx=GpxFormat())

    device_service = DeviceService()
    entry_service = EntryService()

    def get(self, request, device_id):
        response_format = request.query_params.get('accept-type')
        str_datetime = request.query_params.get('datetime')
        entries = self.entry_service.get(device_id, str_datetime)
        if response_format not in self.formats:
            return Response(data=entries)
        selected = self.formats[response_format]
        content_type = f'application/{response_format}'
        return Response(selected.format(entries), content_type=content_type)

    def post(self, request, device_id):
        user_id = request.user.id
        if not self.device_service.exists(user_id):
            if not self.device_service.create(device_id, user_id):
                return Response(status=HTTP_404_NOT_FOUND)
        if not self.entry_service.create(request.data, device_id):
            return Response(status=HTTP_404_NOT_FOUND)
        return Response(status=HTTP_201_CREATED)
