from django.urls import include, path

urlpatterns = [
    path("api/flash/", include("flash.urls")),
]
