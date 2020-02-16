from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_404_NOT_FOUND

from api.models import Device
from api.serializers import DeviceSerializer
from api.services import DeviceService, EntryService
from api.converter import Converter
from api.formats import KmlFormat, GpxFormat


class DevicesView(APIView):
    def get(self, request):
        devices = Device.objects.filter(owner=request.user).order_by('added')
        serializer = DeviceSerializer(instance=devices, many=True)
        return Response({'devices': serializer.data})

    def put(self, request):
        query_set = Device.objects.filter(id=request.data.get('id'))
        query_set.update(name=request.data.get('name'))
        return Response(status=HTTP_200_OK)


class EntriesView(APIView):
    converters = dict(kml=Converter(KmlFormat), gpx=Converter(GpxFormat))

    device_service = DeviceService()
    entry_service = EntryService()

    def get(self, request, device_id):
        response_format = request.query_params.get('accept-type')
        str_datetime = request.query_params.get('datetime')
        entries = self.entry_service.get(device_id, str_datetime)
        if response_format not in self.converters:
            return Response(data={'entries': entries})
        converter = self.converters[response_format]
        content_type = f'application/{response_format}'
        return Response(converter.convert(entries), content_type=content_type)

    def post(self, request, device_id):
        user_id = request.user.id
        if not self.device_service.exists(user_id):
            device_created = self.device_service.create(device_id, user_id)
            if not device_created:
                return Response(status=HTTP_404_NOT_FOUND)
        entry_created = self.entry_service.create(request.data, device_id)
        if not entry_created:
            return Response(status=HTTP_404_NOT_FOUND)
        return Response(status=HTTP_201_CREATED)
