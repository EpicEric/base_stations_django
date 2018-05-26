"""django_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

from base_station.views import (
     index, BasinhoppingView, FSPLView, HeatMapView, SlsqpView, 
     TaguchiView, OptimizationView)
from .api import router


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include((router.urls, 'django_project'), namespace='api')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('', index, name='index'),
    path('optimization/basinhopping', BasinhoppingView.as_view(), name='basinhopping'),
    path('optimization/slsqp', SlsqpView.as_view(), name='slsqp'),
    path('optimization/taguchi', TaguchiView.as_view(), name='taguchi'),
    path('heat-map/', HeatMapView.as_view(), name='heat-map'),
    path('optimization/', OptimizationView.as_view()),
    path('fspl/', FSPLView.as_view())
]
