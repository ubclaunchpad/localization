from django.urls import path
from . import views
from .views import TokenView, TranslationView

urlpatterns = [
    path('token/', TokenView.as_view(), name='create-token'),
    path('token/<str:value>/', TokenView.as_view(), name='read-token'),
    path('translation', TranslationView.as_view(), name='translation'),
    path('translations', views.ProcessTranslationsView.as_view(), name='process-translations')
    path('translations/<str:language/', views.ProcessTranslationsView.as_view(), name='get-translations')
]
