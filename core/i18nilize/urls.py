from django.urls import path
from . import views
from .views import CreateTokenView, ReadTokenView

urlpatterns = [
    path("", views.SampleAPIView.as_view(), name="index"),
    path('token/create/', CreateTokenView.as_view(), name='create-token'),
    path('token/read/<int:pk>/', ReadTokenView.as_view(), name='read-token'),
]