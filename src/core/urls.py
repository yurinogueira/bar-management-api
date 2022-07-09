# coding: utf-8
from django.urls import include, path

from rest_framework.routers import DefaultRouter

from core.views import WeatherViewSet

router = DefaultRouter()

router.register("weather", WeatherViewSet, "weather")

urlpatterns = [
    path("", include(router.urls)),
]
