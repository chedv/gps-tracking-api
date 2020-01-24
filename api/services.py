from .models import Device, Entry
from .serializers import DeviceSerializer, EntrySerializer

from api.utc_datetime import utc_datetime


class Service:
    def save(self, serializer):
        if not serializer.is_valid():
            return False
        serializer.save()
        return True


class DeviceService(Service):
    def create(self, device_id, user_id):
        devices_count = Device.objects.count() + 1
        device_data = {
            'id': device_id,
            'name': 'new device ' + str(devices_count),
            'owner': user_id
        }
        serializer = DeviceSerializer(data=device_data)
        return self.save(serializer)

    def exists(self, user_id):
        return Device.objects.filter(owner=user_id).exists()


class EntryService(Service):
    def create(self, data, device_id):
        entry_data = {
            'latitude': data.get('latitude'),
            'longitude': data.get('longitude'),
            'datetime': data.get('datetime'),
            'device': device_id
        }
        serializer = EntrySerializer(data=entry_data)
        return self.save(serializer)

    def get(self, device_id, str_datetime):
        entries = Entry.objects.filter(device=device_id)
        if str_datetime is not None:
            datetime = utc_datetime(str_datetime)
            entries = entries.filter(device=device_id, datetime__gte=datetime)
        serializer = EntrySerializer(instance=entries.order_by('-datetime'), many=True)
        return serializer.data
