from django.contrib import admin
from django.urls import path
from . import views  # Correct relative import

urlpatterns = [
    path('', views.index, name='index'),
]
