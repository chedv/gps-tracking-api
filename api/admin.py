from django.contrib import admin
from .models import User, Device, Entry


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    pass


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    pass
