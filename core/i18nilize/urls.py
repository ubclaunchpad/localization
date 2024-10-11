from django.urls import path
from . import views
from .views import CreateTokenView, ReadTokenView

urlpatterns = [
    path("", views.SampleAPIView.as_view(), name="index"),
    path('api/token/create/', CreateTokenView.as_view(), name='create-token'),
    path('api/token/read/<int:pk>/', ReadTokenView.as_view(), name='read-token'),
]