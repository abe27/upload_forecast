from django.urls import include, path

from . import views

urlpatterns = [
    path("", views.index),
    path('sync/master', views.sync_master),
]