from django.urls import include, path
from rest_framework import routers

from users.views import CustomUserViewSet

app_name = "api_users"

router_v1 = routers.DefaultRouter()
router_v1.register(r"users", CustomUserViewSet)

urlpatterns = [
    path("", include(router_v1.urls)),
    path("", include("djoser.urls")),
    path("auth/", include("djoser.urls.authtoken")),
]
