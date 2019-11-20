from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED,
                                   HTTP_404_NOT_FOUND)
from rest_framework.authtoken.models import Token

from django.contrib.auth import authenticate, get_user_model

from .models import Device, Entry
from .serializers import DeviceSerializer, EntrySerializer, UserSerializer


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


class DeviceView(APIView):
    def get(self, request):
        devices = Device.objects.filter(owner=request.user).order_by('added')
        serializer = DeviceSerializer(instance=devices, many=True)
        return Response({'devices': serializer.data})

    def put(self, request):
        query_set = Device.objects.filter(id=request.data.get('id'))
        query_set.update(name=request.data.get('name'))
        return Response(status=HTTP_200_OK)


class EntryView(APIView):
    def device_exists(self, user):
        return Device.objects.filter(owner=user).exists()

    def create_device(self, device_id, user):
        device_data = {
            'id': device_id,
            'name': 'new device',
            'owner': user
        }
        serializer = DeviceSerializer(data=device_data)
        if not serializer.is_valid():
            return False
        serializer.save()
        return True

    def create_entry(self, request, device_id):
        entry_data = {
            'latitude': request.data.get('latitude'),
            'longitude': request.data.get('longitude'),
            'datetime': request.data.get('datetime'),
            'device': device_id
        }
        serializer = EntrySerializer(data=entry_data)
        if not serializer.is_valid():
            return False
        serializer.save()
        return True

    def get(self, request, device_id):
        entries = Entry.objects.filter(device=device_id).order_by('datetime')
        serializer = EntrySerializer(instance=entries, many=True)
        return Response({'entries': serializer.data})

    def post(self, request, device_id):
        user = request.user.id
        if not self.device_exists(user):
            if not self.create_device(device_id, user):
                return Response(status=HTTP_404_NOT_FOUND)
        if not self.create_entry(request, device_id):
            return Response(status=HTTP_404_NOT_FOUND)
        return Response(status=HTTP_201_CREATED)
