from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from .models import Pin
from .serializers import PinSerializer
from .filters import PinFilter

class PinViewSet(viewsets.ModelViewSet):
    queryset = Pin.objects.all().order_by('-created_at')
    serializer_class = PinSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = PinFilter

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        pin = self.get_object()
        user = request.user
        if user in pin.likes.all():
            return Response({'status': 'already liked'}, status=status.HTTP_400_BAD_REQUEST)
        pin.likes.add(user)
        return Response({'status': 'liked'})

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def unlike(self, request, pk=None):
        pin = self.get_object()
        user = request.user
        if user not in pin.likes.all():
            return Response({'status': 'not liked yet'}, status=status.HTTP_400_BAD_REQUEST)
        pin.likes.remove(user)
        return Response({'status': 'unliked'})
