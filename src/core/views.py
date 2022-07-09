from collections import deque
from itertools import accumulate

from django.conf import settings

from drf_spectacular.utils import OpenApiParameter, extend_schema
import requests
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from core.serializers import WeatherDataSerializer


class WeatherViewSet(ViewSet):
    authentication_classes: list[object] = []
    permission_classes: list[object] = []
    serializer_class = WeatherDataSerializer

    def get_serializer_class(self, *args, **kwargs):
        return self.serializer_class

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="city",
                location=OpenApiParameter.QUERY,
                description="City name",
                required=True,
                type=str,
            )
        ]
    )
    @action(methods=["get"], detail=False, url_name="search")
    def search(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        city = self.request.GET.get("city", None)

        try:
            parameters = f"?key={settings.WEATHERAPI_KEY}&q={city}&aqi=no"
            url = f"{settings.WEATHERAPI_URL}{parameters}"
            response = requests.post(url)
        except requests.exceptions.HTTPError:
            return Response(status=status.HTTP_404_NOT_FOUND)

        content = response.json()
        prepared_data_fields = [
            ("city", ["location", "name"]),
            ("state", ["location", "region"]),
            ("country", ["location", "country"]),
            ("lat", ["location", "lat"]),
            ("lon", ["location", "lon"]),
            ("timezone", ["location", "tz_id"]),
            ("weather_data", ["current"]),
        ]

        prepared_data = {
            key: deque(accumulate(values, read, initial=content), 1).pop()
            for key, values in prepared_data_fields
            if (read := lambda data, value: data.get(value),)
        }

        serializer = serializer_class(data=prepared_data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
