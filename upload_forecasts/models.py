from datetime import datetime
import uuid
from django.db import models
from django.utils import timezone
from books.models import Book, EDIReviseType

# Create your models here.
class OnMonthList(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, verbose_name="PRIMARY KEY", default=uuid.uuid4)
    name = models.CharField(max_length=250, verbose_name="Name", unique=True, blank=False, null=False)
    value = models.IntegerField(verbose_name="Value", unique=True, blank=False, null=False)
    description = models.TextField(verbose_name="Description",blank=True, null=True)
    is_active = models.BooleanField(verbose_name="Is Active", default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    def short_month_only(self):
        return f"{str(self.name)[:3]}"
    
    def short_month(self):
        mydate = datetime.now()
        onYear = int(mydate.year)
        return f"{str(self.name)[:3]}-{str(onYear)[2:]}"
    
    @classmethod
    def get_default_value_pk(cls):
        mydate = datetime.now()
        onYear = int(mydate.year)
        return cls.objects.get(value=onYear)[0].id
    
    class Meta:
        db_table = "tbmOnMonthList"
        ordering = ("value","name",)
    
class OnYearList(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, verbose_name="PRIMARY KEY", default=uuid.uuid4)
    name = models.CharField(max_length=4, verbose_name="Name", unique=True, blank=False, null=False)
    value = models.IntegerField(verbose_name="Value", unique=True, blank=False, null=False)
    description = models.TextField(verbose_name="Description",blank=True, null=True)
    is_active = models.BooleanField(verbose_name="Is Active", default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    @classmethod
    def get_default_value_pk(cls):
        mydate = datetime.now()
        onMonth = int(mydate.month)
        return cls.objects.get(value=onMonth)[0].id
    
    class Meta:
        db_table = "tbmOnYearList"
        ordering = ("value","name",)
    
class UploadForecast(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, verbose_name="PRIMARY KEY", default=uuid.uuid4)
    file_forecast = models.FileField(upload_to="static/forecasts",verbose_name="File Forecast")
    forecast_date = models.DateField(verbose_name="Date", default=timezone.now, blank=True, null=True)
    forecast_month = models.ForeignKey(OnMonthList, verbose_name="Month", on_delete=models.CASCADE)
    forecast_year = models.ForeignKey(OnYearList, verbose_name="Year", on_delete=models.CASCADE)
    forecast_book_id = models.ForeignKey(Book, verbose_name="Book ID", on_delete=models.CASCADE)
    forecast_revise_id = models.ForeignKey(EDIReviseType, verbose_name="Revise", on_delete=models.CASCADE)
    description = models.TextField(verbose_name="Description",blank=True, null=True)
    is_generated = models.BooleanField(verbose_name="Is Generated", default=False, blank=True, null=True)
    is_active = models.BooleanField(verbose_name="Is Active", default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.forecast_month} {self.forecast_year}"
    
    class Meta:
        db_table = "tbmUploadForecast"
        
class ForecastErrorLogs(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, verbose_name="PRIMARY KEY", default=uuid.uuid4)
    file_name = models.UUIDField(max_length=36, verbose_name="File Forecast")
    row_num = models.IntegerField(verbose_name="Row")
    item = models.IntegerField(verbose_name="Item")
    part_code = models.CharField(max_length=50, verbose_name="Part Code")
    part_no = models.CharField(max_length=50, verbose_name="Part No.")
    part_name = models.CharField(max_length=50, verbose_name="Part Name")
    supplier = models.CharField(max_length=50, verbose_name="Supplier")
    model = models.CharField(max_length=50, verbose_name="Model")
    rev_0 = models.IntegerField(verbose_name="Rev.0",default=0, blank=True, null=True)
    rev_1 = models.IntegerField(verbose_name="Rev.1",default=0, blank=True, null=True)
    rev_2 = models.IntegerField(verbose_name="Rev.2",default=0, blank=True, null=True)
    rev_3 = models.IntegerField(verbose_name="Rev.3",default=0, blank=True, null=True)
    rev_4 = models.IntegerField(verbose_name="Rev.4",default=0, blank=True, null=True)
    rev_5 = models.IntegerField(verbose_name="Rev.5",default=0, blank=True, null=True)
    rev_6 = models.IntegerField(verbose_name="Rev.6",default=0, blank=True, null=True)
    rev_7 = models.IntegerField(verbose_name="Rev.7",default=0, blank=True, null=True)
    remark = models.TextField(verbose_name="Remark", blank=True, null=True)
    is_error = models.BooleanField(verbose_name="Is Error", default=True, blank=True, null=True)
    is_success = models.BooleanField(verbose_name="Is Success", default=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "ediForecastErrorLogs"
        verbose_name = "PDS Error Logging"
        verbose_name_plural = "PDS Error Logging"
        ordering = ('row_num','item','created_at','updated_at')