# events/views.py
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
import asyncio

from .models import Event, Guest
from .serializers import EventSerializer, GuestSerializer
from .storage import upload_file_to_contabo_s3  # Update path!

class EventPhotoUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        file_obj = request.FILES.get("file")
        if not file_obj:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Upload to Contabo (wrap the async uploader into sync context)
            public_url = asyncio.run(upload_file_to_contabo_s3(file_obj))
            return Response({"url": public_url}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get_queryset(self):
        print("EventViewSet get_queryset called")  # Debug üçün
        queryset = Event.objects.all()
        print(f"Found {queryset.count()} events")  # Debug üçün

        # Optional limit parameter
        limit = self.request.query_params.get('limit')
        if limit:
            try:
                limit = int(limit)
                queryset = queryset[:limit]
            except ValueError:
                pass
        return queryset

    def list(self, request, *args, **kwargs):
        print("=" * 50)
        print("EventViewSet.list method çağrıldı")
        queryset = self.get_queryset()
        print(f"URL: {request.path}")
        print(f"Tapılan hadisələr: {queryset.count()}")
        return super().list(request, *args, **kwargs)

class GuestViewSet(viewsets.ModelViewSet):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer