from django.urls import path
from .views import TokenView, MSTokenView, TranslationView, ProcessTranslationsView, PullTranslations, TestTokenView, WriterPermissionView

urlpatterns = [
    path('token/', TokenView.as_view(), name='create-token'),
    path('ms-token/<str:value>/', MSTokenView.as_view(), name='create-ms-token'),
    path('token/<str:value>/', TokenView.as_view(), name='read-token'),
    path('test/', TestTokenView.as_view(), name='test-token'),
    path('translation', TranslationView.as_view(), name='translation'),
    path('translations', ProcessTranslationsView.as_view(), name='process-translations'),
    path('translations/pull/', PullTranslations.as_view(), name='pull-translations'),
    path('translations/push/', TranslationView.as_view(), name='push-translations'),
    path('writer-permission/', WriterPermissionView.as_view(), name='writer-permission'),
]
