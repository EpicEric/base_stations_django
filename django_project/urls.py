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
from django.contrib.auth import views as auth_views
from django.urls import include, path
from rest_framework.authtoken import views

from base_station.views import (
     BasinhoppingView, HeatMapView, SlsqpView,
     TaguchiView, OptimizationView)
from map.views import index
from .api import router


urlpatterns = [
    # Base URLs
    path('admin/', admin.site.urls),
    path('api/', include((router.urls, 'django_project'), namespace='api')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api-token-auth/', views.obtain_auth_token),
    path('login/', auth_views.login, {'template_name': 'admin/login.html'}, name='login'),
    path('logout/', auth_views.logout, name='logout'),
    path('oauth2/', include('rest_framework_social_oauth2.urls')),

    # Demo URLs
    #path('optimization/basinhopping', BasinhoppingView.as_view(), name='basinhopping'),
    #path('optimization/slsqp', SlsqpView.as_view(), name='slsqp'),
    #path('optimization/taguchi', TaguchiView.as_view(), name='taguchi'),
    #path('heat-map/', HeatMapView.as_view(), name='heat-map'),
    #path('optimization/', OptimizationView.as_view()),

    # Index URL
    #path('', index, name='index'),
]
