from django.urls import include, path

from . import views

urlpatterns = [
    path("reports/tags/<str:id>", views.print_tags)
]