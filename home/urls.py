from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Megaverse API",
        default_version='v1',
        description="MVP Backend API Documentation",
        contact=openapi.Contact(email="abdullohxkozimjonov42@gmail.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("main.urls")),
    path("api/docs/", schema_view.with_ui('swagger', cache_timeout=0), name="swagger-ui"),
    path("api/redoc/", schema_view.with_ui('redoc', cache_timeout=0), name="redoc"),
]
