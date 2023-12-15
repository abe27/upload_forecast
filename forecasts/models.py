import uuid
from django.db import models
from django.utils import timezone
from django.utils.html import format_html
from django.db.models import F
from books.models import Book, EDIReviseType

from products.models import Product, ProductGroup
from upload_forecasts.models import OnMonthList, OnYearList, UploadForecast
from members.models import ManagementUser, PlanningForecast, Section, Supplier

FORECAST_ORDER_STATUS = [
    ('0', 'รออนุมัติเปิด PR'),
    ('1', 'อนุมัติเปิด PR'),
    ('2', 'เปิด PR แล้ว'),
    ('3', 'ไม่อนุมัติ'),
]

# Create your models here.
class Forecast(models.Model):
    # REQUEST ORDER
    id = models.UUIDField(primary_key=True, editable=False, verbose_name="PRIMARY KEY", default=uuid.uuid4)
    forecast_plan_id = models.ForeignKey(PlanningForecast, verbose_name="Forecast Plan",blank=True, null=True, on_delete=models.SET_NULL)
    file_forecast_id = models.ForeignKey(UploadForecast, verbose_name="Forecast ID", blank=False, null=False, on_delete=models.CASCADE, editable=False)
    part_model_id = models.ForeignKey(ProductGroup, verbose_name="Model ID", on_delete=models.SET_NULL, null=True, blank=True)
    supplier_id = models.ForeignKey(Supplier, verbose_name="Supplier ID", on_delete=models.SET_NULL, null=True, blank=True)
    section_id = models.ForeignKey(Section, verbose_name="Section ID", blank=True,null=True, on_delete=models.SET_NULL)
    book_id = models.ForeignKey(Book, verbose_name="Book ID", blank=True,null=True, on_delete=models.SET_NULL)
    forecast_revise_id = models.ForeignKey(EDIReviseType,verbose_name="Revise ID", on_delete=models.SET_NULL,null=True, blank=True)
    forecast_on_month_id = models.ForeignKey(OnMonthList,verbose_name="Request On Month", on_delete=models.SET_NULL,null=True, blank=True)
    forecast_on_year_id = models.ForeignKey(OnYearList,verbose_name="Request On Year", on_delete=models.SET_NULL,null=True, blank=True)
    forecast_no = models.CharField(max_length=15,verbose_name="Request No.", blank=True, null=True)
    forecast_date = models.DateField(verbose_name="Request Date", default=timezone.now, null=True, blank=True)
    forecast_item = models.IntegerField(verbose_name="Item", blank=True,null=True, default="0")
    forecast_qty = models.FloatField(verbose_name="Qty.", blank=True,null=True, default="0")
    forecast_total_qty = models.FloatField(verbose_name="Total Qty.", blank=True,null=True, default="0")
    forecast_price = models.FloatField(verbose_name="Price.", blank=True,null=True, default="0")
    forecast_m0 = models.FloatField(verbose_name="Month 0", blank=True, null=True, default="0")
    forecast_m1 = models.FloatField(verbose_name="Month 1", blank=True, null=True, default="0")
    forecast_m2 = models.FloatField(verbose_name="Month 2", blank=True, null=True, default="0")
    forecast_m3 = models.FloatField(verbose_name="Month 3", blank=True, null=True, default="0")
    remark = models.TextField(verbose_name="Remark", blank=True, null=True)
    forecast_by_id = models.ForeignKey(ManagementUser, verbose_name="Request By ID", blank=True, null=True, on_delete=models.SET_NULL)
    forecast_status = models.CharField(max_length=1, choices=FORECAST_ORDER_STATUS,verbose_name="Request Status", default="0")
    forecast_download_count = models.IntegerField(verbose_name="Download Count",  blank=True, null=True, default="0")
    file_estimate_forecast = models.FileField(upload_to="static/estimated_forecasts", verbose_name="Upload Estimated Forecast", blank=True, null=True)
    ref_formula_id = models.CharField(max_length=8, verbose_name="Ref. Formula ID", blank=True, null=True)
    is_po = models.BooleanField(verbose_name="Is PO", default=False, blank=True, null=True)
    is_sync = models.BooleanField(verbose_name="Is Sync", default=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return self.forecast_no
    
    def getattr(self, name):
        print("getattr")
        return self.forecast_no
    
    class Meta:
        db_table = "ediForecast"
        verbose_name = "Forecast"
        verbose_name_plural = "EDI Forecast"
        ordering = ('forecast_status','forecast_date','forecast_no')
        permissions = [
            (
                "approve_reject",
                "จัดการ Approve/Reject"
            ),
            (
                "is_download_report",
                "ดูรายงาน"
            ),
            (
                'upload_file_estimated_forecast',
                'อัพโหลด ESF'
            ),
            (
                'upload_file_forecast',
                'อัพโหลด Forecast'
            )
        ]
        
        default_permissions = ["view",]
class ForecastDetail(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, verbose_name="PRIMARY KEY", default=uuid.uuid4)
    forecast_id = models.ForeignKey(Forecast, verbose_name="Open PDS ID", blank=False, null=False, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, verbose_name="Product Code", blank=False, null=False, on_delete=models.CASCADE)
    seq = models.IntegerField(verbose_name="#", blank=True, null=True,default="0")
    request_qty = models.IntegerField(verbose_name="Request Qty.", default="0.0")
    balance_qty = models.IntegerField(verbose_name="Total Qty.", default="0.0")
    price = models.FloatField(verbose_name="Price.", blank=True,null=True, default="0")
    month_0 = models.IntegerField(verbose_name="Month 0", blank=True, null=True, default="0")
    month_1 = models.IntegerField(verbose_name="Month 1", blank=True, null=True, default="0")
    month_2 = models.IntegerField(verbose_name="Month 2", blank=True, null=True, default="0")
    month_3 = models.IntegerField(verbose_name="Month 3", blank=True, null=True, default="0")
    request_by_id = models.ForeignKey(ManagementUser, verbose_name="Request By ID", blank=True, null=True, on_delete=models.SET_NULL)
    request_status = models.CharField(max_length=1, choices=FORECAST_ORDER_STATUS,verbose_name="Request Status", default="0")
    import_model_by_user = models.CharField(max_length=255, blank=True, null=True, verbose_name="Model")
    remark = models.TextField(verbose_name="Remark", blank=True, null=True)
    is_selected = models.BooleanField(verbose_name="Is Selected", default=False)
    is_sync = models.BooleanField(verbose_name="Is Sync", default=True)
    ref_formula_id = models.CharField(max_length=8, verbose_name="Ref. Formula ID", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return ""
    
    def product_no(self):
        return str(self.product_id.code)
    
    def product_code(self):
        return str(self.product_id.no)
    
    def product_name(self):
        return str(self.product_id.name)
    
    def product_group(self):
        # return str(self.product_id.prod_group_id.code)
        return format_html(f"<span class='text-danger text-bold'>{self.product_id.prod_group_id.code}</span>")
    
    def last_updated(self):
        return self.updated_at.strftime("%d-%m-%Y %H:%M:%S")
    
    class Meta:
        db_table = "ediForecastDetail"
        verbose_name = "ForecastDetail"
        verbose_name_plural = "Forecast Detail"
        ordering = ('seq','product_id','created_at','updated_at')
        permissions = [
            (
                "edit_qty_price",
                "แก้ไขจำนวนและราคา"
            ),
            (
                "select_item",
                "เลือกรายการสินค้า"
            )
        ]