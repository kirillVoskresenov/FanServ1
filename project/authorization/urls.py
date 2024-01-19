from django.urls import path
from .views import AuthView

urlpatterns = [
    path('accounts/profile/', AuthView.as_view())
]