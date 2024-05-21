from rest_framework import serializers
from .models import Pin

class PinSerializer(serializers.ModelSerializer):

    class Meta:
        model = Pin
        fields = '__all__'
        read_only_fields = ['user']

class PinLikeSerializer(serializers.Serializer):
    id = serializers.IntegerField()

    def validate_id(self, value):
        if not Pin.objects.filter(id=value).exists():
            raise serializers.ValidationError("Pin with this ID does not exist.")
        return value