"""HypeBack URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls import include
from django.contrib import admin
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import path, re_path
from django.views.generic import RedirectView
from django.views.static import serve

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

# Admin
# ---------------------------------------------------------------------------
favicon = RedirectView.as_view(url=staticfiles_storage.url("favicon.ico"))

# Media Roots
# ----------------------------------------------------------------------------
MEDIA_ROOT = {"document_root": settings.MEDIA_ROOT}
STATIC_ROOT = {"document_root": settings.STATIC_ROOT}

# Token Authentication
# ----------------------------------------------------------------------------
token_obtain_pair = TokenObtainPairView.as_view()
token_refresh = TokenRefreshView.as_view()
token_verify = TokenVerifyView.as_view()

# DRF Spectacular Swagger
# ----------------------------------------------------------------------------
schema = SpectacularAPIView.as_view()
swagger = SpectacularSwaggerView.as_view(url_name="schema")

urlpatterns = [
    # Admin
    # ------------------------------------------------------------------------
    path("admin/", admin.site.urls),
    path("favicon.ico", favicon),
    # Media Contents
    # ------------------------------------------------------------------------
    re_path(r"^media/(?P<path>.*)$", serve, MEDIA_ROOT),
    re_path(r"^static/(?P<path>.*)$", serve, STATIC_ROOT),
    # Apps
    # ------------------------------------------------------------------------
    path("users/", include(("users.urls", "users")), name="users"),
    path("members/", include(("members.urls", "members")), name="members"),
    # Authentication
    # ------------------------------------------------------------------------
    path("auth/token/", token_obtain_pair, name="token_obtain_pair"),
    path("auth/token/refresh/", token_refresh, name="token_refresh"),
    path("auth/token/verify/", token_verify, name="token_verify"),
    # Swagger
    # ------------------------------------------------------------------------
    path("docs/", swagger, name="swagger-ui"),
    path("docs/generate/", schema, name="schema"),
]
