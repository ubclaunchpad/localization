from django.urls import path

from . import views

urlpatterns = [
    path("", views.SampleAPIView.as_view(), name="index"),
    path("updatedb", views.PostTranslations.as_view(), name="updatedb")
]
