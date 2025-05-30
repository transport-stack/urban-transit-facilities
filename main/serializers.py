from rest_framework import serializers


class StatusSerializer(serializers.Serializer):
    status = serializers.CharField()
    system_time = serializers.CharField()
