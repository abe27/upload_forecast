from django.contrib import admin
from .models import Forecast

# Register your models here.
class ForecastAdmin(admin.ModelAdmin):
    pass

admin.site.register(Forecast, ForecastAdmin)