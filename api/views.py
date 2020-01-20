from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_404_NOT_FOUND

from .models import Device
from .serializers import DeviceSerializer
from .services import DeviceService, EntryService
from .exporter import Exporter


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
    device_service = DeviceService()
    entry_service = EntryService()

    def get(self, request, device_id):
        export_type = request.query_params.get('type')
        str_datetime = request.query_params.get('datetime')
        entries = self.entry_service.get(device_id, str_datetime)
        try:
            result = Exporter().export(entries, export_type)
            return Response(data=result, content_type='application/%s' % export_type)
        except KeyError:
            return Response(status=HTTP_404_NOT_FOUND)

    def post(self, request, device_id):
        user_id = request.user.id
        if not self.device_service.exists(user_id):
            if not self.device_service.create(device_id, user_id):
                return Response(status=HTTP_404_NOT_FOUND)
        if not self.entry_service.create(request, device_id):
            return Response(status=HTTP_404_NOT_FOUND)
        return Response(status=HTTP_201_CREATED)
