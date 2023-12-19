from django.urls import include, path

from . import views

urlpatterns = [
    path("", views.index),
    path('download_pds/<str:id>', views.download_pds),
    path('report_pds/', views.report_pds),
]