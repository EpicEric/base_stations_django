from django.urls import path

from .views import BasinhoppingView, HeatMapView, SlsqpView, TaguchiView

app_name = 'demo'
urlpatterns = [
    path('optimization/basinhopping', BasinhoppingView.as_view(), name='basinhopping'),
    path('optimization/slsqp', SlsqpView.as_view(), name='slsqp'),
    path('optimization/taguchi', TaguchiView.as_view(), name='taguchi'),
    path('heat-map/', HeatMapView.as_view(), name='heat-map'),
    # path('optimization/', OptimizationView.as_view()),
    # path('fspl/', FSPLView.as_view())
]
