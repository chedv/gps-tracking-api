from rest_framework.serializers import ModelSerializer, ValidationError
from .models import Device, Entry


class DeviceSerializer(ModelSerializer):
    class Meta:
        model = Device
        fields = ('id', 'name', 'owner')
        extra_kwargs = {
            'owner': {'write_only': True}
        }


class EntrySerializer(ModelSerializer):
    def _validate_latitude(self, attrs):
        if not -90.0 <= attrs['latitude'] <= 90.0:
            raise ValidationError("Invalid latitude value. It must be in range [-90.0, 90.0]")

    def _validate_longitude(self, attrs):
        if not -180.0 <= attrs['longitude'] <= 180.0:
            raise ValidationError("Invalid longitude value. It must be in range [-180.0, 180.0]")

    def _validate_satellites(self, attrs):
        if 'satellites' in attrs and attrs['satellites'] is not None and not 3 <= attrs['satellites'] <= 16:
            raise ValidationError("Invalid satellites number. It must be in range [3, 16]")

    def validate(self, attrs):
        self._validate_latitude(attrs)
        self._validate_longitude(attrs)
        self._validate_satellites(attrs)
        return super().validate(attrs)

    class Meta:
        model = Entry
        fields = ('latitude', 'longitude', 'datetime', 'satellites', 'device')
        extra_kwargs = {
            'device': {'write_only': True}
        }
