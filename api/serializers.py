from rest_framework.serializers import ModelSerializer
from .models import Device, Entry


class DeviceSerializer(ModelSerializer):
    class Meta:
        model = Device
        fields = ('id', 'name', 'owner')
        extra_kwargs = {
            'owner': {'write_only': True}
        }


class EntrySerializer(ModelSerializer):
    class Meta:
        model = Entry
        fields = ('latitude', 'longitude', 'datetime', 'device')
        extra_kwargs = {
            'device': {'write_only': True}
        }
