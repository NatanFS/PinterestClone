# apps/pins/urls.py

from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import PinViewSet

router = DefaultRouter()
router.register(r'pins', PinViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
