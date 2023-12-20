"""
URL configuration for webbase project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.views.generic import RedirectView
from django.contrib import admin
from django.urls import include, path
from confirm_invoices.models import ConfirmInvoiceHeader

from forecasts.models import Forecast
from open_pds.models import PDSHeader
from receives.models import ReceiveHeader
from receives import apps as receive_apps
from confirm_invoices import apps as confirm_invoice_apps

admin.site.site_title = "EDI Web Application"
admin.site.site_header = "EDI Web Application"
admin.site.index_title = "EDI Management System"
# admin.site.site_url = "/"
# admin.site.enable_nav_sidebar = True
admin.site.empty_value_display = "-"

# admin.autodiscover()
# admin.site.enable_nav_sidebar = True
Forecast._meta.verbose_name_plural = "Upload Forecast"
PDSHeader._meta.verbose_name_plural = "Open PDS"
ConfirmInvoiceHeader._meta.verbose_name_plural = "View Purchase"
confirm_invoice_apps.ConfirmInvoicesConfig.verbose_name = "คำสั่งซื้อสินค้า"
ReceiveHeader._meta.verbose_name_plural = "View Receive"
receive_apps.ReceivesConfig.verbose_name = "จัดการข้อมูล Receive"

urlpatterns = [
    path("web/", include('validate_requests.urls')),
    path('web/', admin.site.urls),
    path("forecast/", include("forecasts.urls"), name="forecast"),
    path("open_pds/", include("open_pds.urls"), name="open_pds"),
    path("receives/", include("receives.urls"), name="receive"),
    path("confirm_invoices/", include("confirm_invoices.urls"), name="confirm_invoices"),
    # path(""),
    path("", RedirectView.as_view(url="/web/", permanent=True)),
]
