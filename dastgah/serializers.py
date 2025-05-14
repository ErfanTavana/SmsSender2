from rest_framework import serializers
from .models import Device, DeviceLog


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ['id', 'uid', 'name', 'location', 'description']


class DeviceLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceLog
        fields = [
            'id', 'device', 'timestamp', 'level', 'message',
            'module', 'code', 'extra_data'
        ]
