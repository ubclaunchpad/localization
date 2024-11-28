from django.urls import path
from .views import TokenView, TranslationView, ProcessTranslationsView, PullTranslations, GetTokens

urlpatterns = [
    path('token/', TokenView.as_view(), name='create-token'),
    path('token/<str:value>/', TokenView.as_view(), name='read-token'),
    path('translation', TranslationView.as_view(), name='translation'),
    path('translations', ProcessTranslationsView.as_view(), name='process-translations'),
    path('translations/pull', PullTranslations.as_view(), name='pull-translations'),
]
