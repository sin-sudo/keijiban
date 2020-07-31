from django.urls import path

from .views import accounts_views

urlpatterns = [
  path('signup/', accounts_views, name = "signup"),
]