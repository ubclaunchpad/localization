from django.urls import path
from . import views
from .views import TokenView

urlpatterns = [
    path("", views.SampleAPIView.as_view(), name="index"),
    path('token/', TokenView.as_view(), name='create-token'),
    path('token/<str:value>/', TokenView.as_view(), name='read-token'), 
]