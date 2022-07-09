from django.urls import reverse

import pytest
from rest_framework import status


@pytest.mark.django_db
class TestWeatherViewSetViewSet:
    @pytest.mark.vcr(filter_query_parameters=[("key", None)])
    def test_search(self, api_client):
        """Ensure that post router works"""
        url = f"{reverse('core:weather-search')}?city=tangua"

        response = api_client.get(url)
        content = response.json()

        assert content.get("city") == "Tangua"
        assert content.get("state") == "Rio de Janeiro"
        assert content.get("country") == "Brazil"
        assert response.status_code == status.HTTP_200_OK
