from rest_framework import serializers
from django.utils import timezone
from rest_framework.serializers import ModelSerializer
from django.db import models


class CustomDateTimeField(serializers.DateTimeField):
    def to_representation(self, value):
        tz = timezone.get_default_timezone()
        # timezone.localtime() defaults to the current tz, you only
        # need the `tz` arg if the current tz != default tz
        value = timezone.localtime(value, timezone=tz)
        return super().to_representation(value)


class TZAwareModelSerializer(ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(TZAwareModelSerializer, self).__init__(*args, **kwargs)
        self.serializer_field_mapping[models.DateTimeField] = CustomDateTimeField
