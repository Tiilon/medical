from .views import *
from django.urls import path

urlpatterns = [
    path('profile/', ProfileView.as_view()),
]