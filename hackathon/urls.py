from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("iuu.urls")),
    path("", include("funding.urls")),
]

