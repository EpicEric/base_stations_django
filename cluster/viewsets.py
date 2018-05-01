from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from base_station.models import IdentifiedBaseStation
from .models import Cluster
from .serializers import ClusterSerializer


class ClusterViewSet(GenericViewSet):
    queryset = IdentifiedBaseStation.objects.all().order_by('id')
    serializer_class = ClusterSerializer

    def list(self, request, *args, **kwargs):
        # Get tile parameters
        try:
            x_tile = int(self.request.query_params['x_tile'])
            y_tile = int(self.request.query_params['y_tile'])
            zoom_size = int(self.request.query_params['zoom_size'])
        except KeyError as e:
            raise ValueError("Missing parameter: {}".format(e.args[0]))

        cluster_list = Cluster.get_clusters(x_tile, y_tile, zoom_size)
        serializer = self.get_serializer(cluster_list)
        return Response(serializer.data)
