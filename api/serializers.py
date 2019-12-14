from rest_framework.serializers import ModelSerializer
from django.contrib.auth import get_user_model

from .models import Device, Entry


class UserSerializer(ModelSerializer):
    def create(self, validated_data):
        user = get_user_model().objects.create(
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = get_user_model()
        fields = ('email', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }


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
