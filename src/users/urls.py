# coding: utf-8
from django.conf.urls import include
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from rest_framework.routers import DefaultRouter

from users.views import ResetPasswordViewSet, UserViewSet

RESET_PASSWORD_VIEW = csrf_exempt(ResetPasswordViewSet.as_view())

router = DefaultRouter()
router.register("user", UserViewSet, "user")

urlpatterns = [
    path("password/reset/", RESET_PASSWORD_VIEW, name="reset-password"),
    path("", include(router.urls)),
]
