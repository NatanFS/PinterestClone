from rest_framework import viewsets
from .models import Pin
from .serializers import PinSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class PinViewSet(viewsets.ModelViewSet):
    queryset = Pin.objects.all().order_by('-created_at')
    serializer_class = PinSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]