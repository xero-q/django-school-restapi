from django.urls import path
from .views import HomeView

urlpatterns = [
    path('api/home', HomeView.as_view(), name='home-api'),
]