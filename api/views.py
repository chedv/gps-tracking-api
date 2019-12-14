from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_404_NOT_FOUND
from rest_framework.authtoken.models import Token

from django.contrib.auth import authenticate, get_user_model

from .models import Device
from .serializers import DeviceSerializer, UserSerializer
from .services import DeviceService, EntryService

import simplekml


class UserRegisterView(CreateAPIView):
    permission_classes = (AllowAny,)
    model = get_user_model()
    serializer_class = UserSerializer


class UserLoginView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request=request, email=email, password=password)
        if user is None:
            return Response({'error': 'Invalid email or password'})
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})


class UserLogoutView(APIView):
    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=HTTP_200_OK)


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
        str_datetime = request.query_params.get('datetime')
        entries = self.entry_service.get(device_id, str_datetime)
        return Response({'entries': entries})

    def post(self, request, device_id):
        user_id = request.user.id
        if not self.device_service.exists(user_id):
            if not self.device_service.create(device_id, user_id):
                return Response(status=HTTP_404_NOT_FOUND)
        if not self.entry_service.create(request, device_id):
            return Response(status=HTTP_404_NOT_FOUND)
        return Response(status=HTTP_201_CREATED)


class EntriesExportView(APIView):
    entry_service = EntryService()

    def create_kml(self, entries):
        kml = simplekml.Kml()
        for i, entry in enumerate(entries):
            name = 'Point #%d' % (i+1)
            coord = (entry['latitude'], entry['longitude'])
            point = kml.newpoint(name=name, coords=[coord])
            point.timestamp.when = entry['datetime']
        return kml.kml()

    def get(self, request, device_id):
        str_datetime = request.query_params.get('datetime')
        entries = self.entry_service.get(device_id, str_datetime)
        kml = self.create_kml(entries)
        return Response(data=kml, content_type='application/kml')
