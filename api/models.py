from django.contrib.auth import get_user_model
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin,
                                        BaseUserManager)
from django.db import models


class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email must be set')
        email = self.normalize_email(email=email)
        user = self.model(email=email, **extra_fields)
        user.set_password(raw_password=password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email=email, password=password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, null=False)
    is_staff = models.BooleanField(verbose_name='staff status', default=False,)
    is_active = models.BooleanField(verbose_name='active', default=True,)
    objects = UserManager()
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email


class Device(models.Model):
    id = models.CharField(max_length=16, primary_key=True)
    name = models.CharField(max_length=32)
    added = models.DateTimeField(auto_now_add=True, db_index=True)
    owner = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Entry(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    datetime = models.DateTimeField(db_index=True)
    device = models.ForeignKey(to=Device, on_delete=models.CASCADE)

    def get_str_date(self):
        return self.datetime.strftime('%d/%m/%Y')

    def get_str_time(self):
        return self.datetime.strftime('%H:%M:%S')

    def __str__(self):
        to_format = 'latitude: {:f} longitude: {:f} {} {}'
        return to_format.format(self.latitude, self.longitude,
                                self.get_str_date(), self.get_str_time())
