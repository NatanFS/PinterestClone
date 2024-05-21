from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from .models import Pin
from .serializers import PinSerializer
from .filters import PinFilter
from rest_framework.pagination import PageNumberPagination

class PinViewSet(viewsets.ModelViewSet):
    queryset = Pin.objects.all().order_by('-created_at')
    serializer_class = PinSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = PinFilter
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        pin = self.get_object()
        if request.user in pin.likes.all():
            pin.likes.remove(request.user)
            liked = False
        else:
            pin.likes.add(request.user)
            liked = True
        pin.save()
        return Response({'likes': pin.likes.count(), 'liked': liked}, status=status.HTTP_200_OK)

