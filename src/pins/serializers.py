from rest_framework import serializers
from pins.models import Pin
from users.serializer import UserSerializer

class PinSerializer(serializers.ModelSerializer):

    class Meta:
        model = Pin
        fields = '__all__'
        read_only_fields = ['user']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user'] = UserSerializer(instance.user).data
        return response

class PinLikeSerializer(serializers.Serializer):
    id = serializers.IntegerField()

    def validate_id(self, value):
        if not Pin.objects.filter(id=value).exists():
            raise serializers.ValidationError("Pin with this ID does not exist.")
        return value