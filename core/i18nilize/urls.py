from django.urls import path

from . import views

urlpatterns = [
    path("", views.SampleAPIView.as_view(), name="index"),
]