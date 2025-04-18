from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EventPhotoUploadView, EventViewSet, GuestViewSet

router = DefaultRouter()
router.register(r'events', EventViewSet)
router.register(r'guests', GuestViewSet)

urlpatterns = [
    path('upload-photo/', EventPhotoUploadView.as_view(), name='event-photo-upload'),
    path('', include(router.urls)),  # Bütün REST API URL'lərini əlavə edir
]