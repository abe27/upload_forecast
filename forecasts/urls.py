from django.urls import include, path

from . import views

urlpatterns = [
    path("", views.index),
    # path('logging/<str:id>', views.export_excel),
    # path('create_po/<str:id>', views.create_po_forecast),
    path('approve/<str:id>', views.approve_forecast),
    # path('download/<str:id>', views.download_forecast),
    # path('export_pds/<str:id>', views.download_open_pds),
    # path('estimated_forecast/<str:id>', views.estimated_report),
    path('export_forecast/<str:id>', views.export_forecast),
]