from rest_framework_dataclasses.serializers import DataclassSerializer

from core.models import WeatherData


class WeatherDataSerializer(DataclassSerializer):
    class Meta:
        dataclass = WeatherData
