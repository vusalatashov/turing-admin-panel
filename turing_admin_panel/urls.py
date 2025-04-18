# turing_admin_panel/urls.py
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from events.views import EventViewSet, GuestViewSet

router = DefaultRouter()
router.register(r'events', EventViewSet)
router.register(r'guests', GuestViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    # Yalnız bir API endpoint təyin edin
    path('api/v1/', include(router.urls)),
    # Photo upload kimi spesifik URL'lər üçün
    path('api/v1/', include('events.urls')),
]