from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from .serializers import MapInfoSerializer


class MapInfoViewSet(ViewSet):
    def list(self, request, format=None):
        serializer = MapInfoSerializer(request)
        return Response(serializer.data)
