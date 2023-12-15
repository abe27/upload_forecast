import uuid
from django.db import models
from books.models import EDIReviseType

from forecasts.models import FORECAST_ORDER_STATUS, Forecast, ForecastDetail
from products.models import ProductGroup
from upload_forecasts.models import OnMonthList, OnYearList
from members.models import ManagementUser, PlanningForecast, Supplier

FORECAST_PDS_STATUS = [
    (0, "รอเปิด PDS"),
    (1, "เปิด PDS บางส่วน"),
    (2, "เสร็จสมบูรณ์"),
    (3, "ยกเลิก"),
    (4, "-"),
]

# Create your models here.
class PDSHeader(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, verbose_name="PRIMARY KEY", default=uuid.uuid4)
    approve_by_id = models.ForeignKey(ManagementUser, verbose_name="Approve By ID", blank=True, null=True, on_delete=models.SET_NULL)
    forecast_id = models.ForeignKey(Forecast, verbose_name="PR No.", blank=False, null=False, on_delete=models.CASCADE, editable=False)
    supplier_id = models.ForeignKey(Supplier, verbose_name="Supplier ID", blank=True, null=True, on_delete=models.SET_NULL)
    part_model_id = models.ForeignKey(ProductGroup, verbose_name="Model ID", on_delete=models.SET_NULL, null=True, blank=True)
    forecast_plan_id = models.ForeignKey(PlanningForecast, blank=True, null=True, on_delete=models.SET_NULL, verbose_name="Forecast Plan")
    pds_date = models.DateField(verbose_name="PDS Date", blank=True, null=True)
    pds_delivery_date = models.DateField(verbose_name="Delivery Date", blank=True, null=True)
    pds_no = models.CharField(max_length=15,verbose_name="PDS No.", blank=True, null=True)
    pds_revise_id = models.ForeignKey(EDIReviseType,verbose_name="Revise ID", on_delete=models.SET_NULL,null=True, blank=True)
    pds_on_month_id = models.ForeignKey(OnMonthList,verbose_name="Request On Month", on_delete=models.SET_NULL,null=True, blank=True)
    pds_on_year_id = models.ForeignKey(OnYearList,verbose_name="Request On Year", on_delete=models.SET_NULL,null=True, blank=True)
    item = models.IntegerField(verbose_name="Item")
    qty = models.IntegerField(verbose_name="Qty")
    balance_qty = models.IntegerField(verbose_name="Total Qty", blank=True, null=True, default="0")
    summary_price = models.FloatField(verbose_name="Summary Price", blank=True, null=True, default="0")
    # total_item = models.IntegerField(verbose_name="Item", blank=True, null=True, default="0")
    # total_qty = models.IntegerField(verbose_name="Qty", blank=True, null=True, default="0")
    # total_balance_qty = models.IntegerField(verbose_name="Total Qty", blank=True, null=True, default="0")
    # total_summary_price = models.FloatField(verbose_name="Summary Price", blank=True, null=True, default="0")
    remark = models.TextField(verbose_name="Remark", blank=True, null=True)
    pds_status = models.CharField(max_length=1, choices=FORECAST_PDS_STATUS,verbose_name="PDS Status", blank=True, null=True, default="0")
    pds_download_count = models.IntegerField(verbose_name="Download Count", blank=True, null=True)
    ref_formula_id = models.CharField(max_length=8, blank=True, null=True, verbose_name="Formula ID")
    is_active = models.BooleanField(verbose_name="Is Active", default=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.pds_no)
    
    class Meta:
        db_table = "ediPDS"
        verbose_name = "PDS"
        verbose_name_plural = "EDI PDS"
        ordering = ('pds_status','pds_no','created_at','updated_at')
        permissions = [
            (
                "create_purchase_order",
                "เปิด PO"
            ),
            (
                "is_download_report",
                "ดูรายงาน"
            ),
            (
                "add_new_item",
                "เพิ่มรายการใหม่"
            ),
            (
                "edit_qty",
                "แก้ไขจำนวน"
            ),
            (
                "edit_price",
                "แก้ไขราคา"
            ),
            (
                "print_tag",
                "Print TAG"
            )
        ]
        
class PDSDetail(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, verbose_name="PRIMARY KEY", default=uuid.uuid4)
    pds_header_id = models.ForeignKey(PDSHeader, verbose_name="PDS ID", blank=False, null=False, on_delete=models.CASCADE, editable=False)
    forecast_detail_id = models.ForeignKey(ForecastDetail, verbose_name="PDS Detail", on_delete=models.CASCADE)
    seq = models.IntegerField(verbose_name="Seq.")
    qty = models.IntegerField(verbose_name="Qty")
    balance_qty = models.IntegerField(verbose_name="Total Qty", blank=True, null=True, default="0")
    price = models.FloatField(verbose_name="Price", blank=True, null=True, default="0")
    # total_seq = models.IntegerField(verbose_name="Seq.", blank=True, null=True, default="0")
    # total_qty = models.IntegerField(verbose_name="Qty", blank=True, null=True, default="0")
    # total_balance_qty = models.IntegerField(verbose_name="Total Qty", blank=True, null=True, default="0")
    # total_price = models.FloatField(verbose_name="Price", blank=True, null=True, default="0")
    remark = models.TextField(verbose_name="Remark", blank=True, null=True)
    ref_formula_id = models.CharField(max_length=8, blank=True, null=True, verbose_name="Formula ID")
    is_select = models.BooleanField(verbose_name="Is Select", blank=True, null=True, default=True)
    is_active = models.BooleanField(verbose_name="Is Active", default=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.forecast_detail_id)
    
    def product_no(self):
        return str(self.forecast_detail_id.product_id.code)
    
    def product_code(self):
        return str(self.forecast_detail_id.product_id.no)
    
    def product_name(self):
        return str(self.forecast_detail_id.product_id.name)
    
    def get_model(self):
        return str(self.forecast_detail_id.import_model_by_user)
    
    class Meta:
        db_table = "ediPDSDetail"
        verbose_name = "PDSDetail"
        verbose_name_plural = "PDS Detail"
        ordering = ('seq','forecast_detail_id','created_at','updated_at')
        # permissions = [
        #     (
        #         "create_purchase_order",
        #         "เปิด PO"
        #     ),
        #     (
        #         "edit_purchase_qty_price",
        #         "แก้ไขจำนวน/ราคา"
        #     )
        # ]
        
class ReportPDSHeader(models.Model):
    delivery_date = models.CharField(max_length=50,verbose_name="Delivery Date")# ParmDeliveryDate
    sup_code = models.CharField(max_length=50, verbose_name="Sup. Code")# ParmSupCode
    sup_name = models.CharField(max_length=255, verbose_name="Sup. Name")# ParmSumName
    sup_telephone = models.CharField(max_length=50, verbose_name="Sup. Telephone", blank=True, null=True)# ParmSupTelephone
    pds_no = models.CharField(max_length=50,unique=True,verbose_name="PDS No.")# ParmPDSNo
    issue_date = models.CharField(max_length=50, verbose_name="Issue Date")# ParmIssueDate
    issue_time = models.CharField(max_length=50, verbose_name="Issue Time", blank=True, null=True)# ParmTime
    approve_by_id = models.ImageField(verbose_name="Approve By ID",blank=True, null=True)
    issue_by_id = models.ImageField(verbose_name="Issue By ID",blank=True, null=True)
    is_active = models.BooleanField(verbose_name="Is Active", default=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    class Meta:
        db_table = "tempReportPDSHeader"
        

class ReportPDSDetail(models.Model):
    pds_no = models.ForeignKey(ReportPDSHeader, verbose_name="PDS Header", on_delete=models.CASCADE)
    seq = models.IntegerField(verbose_name="Seq.")
    part_model = models.CharField(max_length=50, verbose_name="Part Model", blank=True, null=True)# itemPartCode
    part_code = models.CharField(max_length=50, verbose_name="Part Code")# itemPartCode
    part_name = models.CharField(max_length=255, verbose_name="Part Name")# itemPartName
    packing_qty = models.IntegerField(verbose_name="Packing")# itemPartPack
    total = models.IntegerField(verbose_name="Total")# itemTotal
    is_active = models.BooleanField(verbose_name="Is Active", default=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    class Meta:
        db_table = "tempReportPDSDetail"