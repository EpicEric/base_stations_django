from collections import OrderedDict
from rest_framework.serializers import BaseSerializer


class ClusterSerializer(BaseSerializer):
    def to_representation(self, data):
        """
        Add GeoJSON compatible formatting to a serialized queryset list
        """
        return OrderedDict((
            ("type", "FeatureCollection"),
            ("count", len(data)),
            ("features", list(
                map(lambda c: OrderedDict((
                    ("type", "Feature"),
                    ("geometry", OrderedDict((
                        ("type", "Point"),
                        ("coordinates", [c.point.x, c.point.y])
                    ))),
                    ("properties", OrderedDict((
                        ("count", c.count),
                        ("cgi", c.cgi)
                    )))
                )), data)
            ))
        ))
