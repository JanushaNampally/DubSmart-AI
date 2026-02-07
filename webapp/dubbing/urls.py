from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("start/", views.start),
    path("logs/", views.logs),
    path("status/", views.status),
]
