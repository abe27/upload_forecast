from django.urls import include, path

from . import views

urlpatterns = [
    path("", views.index),
    path("reports/pds/<str:id>", views.pds_reports),
    path("reports/tags/<str:id>", views.print_tags),
    path("reports/purchase/<str:id>", views.export_purchase)
]