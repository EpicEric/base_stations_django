var CustomClusterIcon = L.Icon.extend({
    options: {
        iconSize:   [45, 45],
        iconAnchor: [22, 22]
    }
});
var customClusterSmall = new CustomClusterIcon({iconUrl: '/static/leaflet_plugin/images/custom_cluster_small.png'}),
    customClusterMedium = new CustomClusterIcon({iconUrl: '/static/leaflet_plugin/images/custom_cluster_medium.png'}),
    customClusterBig = new CustomClusterIcon({iconUrl: '/static/leaflet_plugin/images/custom_cluster_big.png'});