import uuid
from django.db import models
from open_pds.models import PDSDetail, PDSHeader
from products.models import ProductGroup

from members.models import ManagementUser, Supplier

CONFIRM_INV_STATUS = [
    ("0", "รอยืนยัน"),
    ("1", "ยืนยันแล้ว"),
    ("2", "ยืนยันบางส่วน"),
    ("3", "ยกเลิก"),### ("3", "ยกเลิกจาก PDS"),
    ("4", "ยกยอด"),
]
# Create your models here.
class ConfirmInvoiceHeader(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, verbose_name="PRIMARY KEY", default=uuid.uuid4)
    approve_by_id = models.ForeignKey(ManagementUser, verbose_name="Approve By ID", blank=True, null=True, on_delete=models.SET_NULL)
    pds_id = models.ForeignKey(PDSHeader, verbose_name="PR No.", blank=False, null=False, on_delete=models.CASCADE, editable=False)
    supplier_id = models.ForeignKey(Supplier, verbose_name="Supplier ID", blank=True, null=True, on_delete=models.SET_NULL)
    part_model_id = models.ForeignKey(ProductGroup, verbose_name="Model ID", on_delete=models.SET_NULL, null=True, blank=True)
    purchase_no = models.CharField(max_length=15,verbose_name="PO No.", blank=True, null=True)
    inv_date = models.DateField(verbose_name="Invoice Date", blank=True, null=True)
    inv_delivery_date = models.DateField(verbose_name="Delivery Date", blank=True, null=True)
    inv_no = models.CharField(max_length=15,verbose_name="Invoice No.", blank=True, null=True)
    item = models.IntegerField(verbose_name="Item")
    qty = models.IntegerField(verbose_name="Qty")
    confirm_qty = models.IntegerField(verbose_name="Confirm Qty", blank=True, null=True, default="0")
    original_qty = models.IntegerField(verbose_name="Original Qty", blank=True, null=True, default="0")
    summary_price = models.FloatField(verbose_name="Summary Price", blank=True, null=True, default="0")
    remark = models.TextField(verbose_name="Remark", blank=True, null=True)
    inv_status = models.CharField(max_length=1, choices=CONFIRM_INV_STATUS,verbose_name="inv Status", blank=True, null=True, default="0")
    ref_formula_id = models.CharField(max_length=8, blank=True, null=True, verbose_name="Formula ID")
    is_download_count = models.IntegerField(verbose_name="Download Count", blank=True, null=True, default="0")
    is_active = models.BooleanField(verbose_name="Is Active", default=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        if self.inv_no is None:
            return str(self.id)
        
        return str(self.inv_no)
    
    class Meta:
        db_table = "ediConfirmInvoice"
        verbose_name = "Confirm Invoice"
        verbose_name_plural = "EDI Confirm Invoice"
        ordering = ('inv_status','inv_no','updated_at')
        permissions = [
            (
                "is_download_report",
                "ดูรายงาน"
            ),
            (
                "edit_qty",
                "แก้ไขจำนวน"
            ),
            (
                "print_tag",
                "Print TAG"
            )
        ]
        
class ConfirmInvoiceDetail(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, verbose_name="PRIMARY KEY", default=uuid.uuid4)
    invoice_header_id = models.ForeignKey(ConfirmInvoiceHeader, verbose_name="PDS ID", blank=False, null=False, on_delete=models.CASCADE, editable=False)
    pds_detail_id = models.ForeignKey(PDSDetail, verbose_name="PDS Detail", on_delete=models.CASCADE)
    seq = models.IntegerField(verbose_name="Seq.")
    qty = models.IntegerField(verbose_name="Qty")
    confirm_qty = models.IntegerField(verbose_name="Confirm Qty", blank=True, null=True, default="0")
    total_qty = models.IntegerField(verbose_name="Total Qty", blank=True, null=True, default="0")
    balance_qty = models.IntegerField(verbose_name="Total Qty", blank=True, null=True, default="0")
    price = models.FloatField(verbose_name="Price", blank=True, null=True, default="0")
    remark = models.TextField(verbose_name="Remark", blank=True, null=True)
    ref_formula_id = models.CharField(max_length=8, blank=True, null=True, verbose_name="Formula ID")
    confirm_status = models.CharField(max_length=1, blank=True, null=True, verbose_name="Status", default="0", choices=CONFIRM_INV_STATUS)
    is_select = models.BooleanField(verbose_name="Is Select", blank=True, null=True, default=True)
    is_active = models.BooleanField(verbose_name="Is Active", default=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.pds_detail_id)
    
    def product_code(self):
        return str(self.pds_detail_id.forecast_detail_id.product_id.no)
    
    def product_no(self):
        return str(self.pds_detail_id.forecast_detail_id.product_id.code)
    
    def product_name(self):
        return str(self.pds_detail_id.forecast_detail_id.product_id.name)
    
    def total(self):
        if self.qty > 0:
            return self.qty
        
        return self.total_qty
    
    def last_update(self):
        return self.updated_at.strftime("%Y-%m-%d %H:%M:%S")
    
    class Meta:
        db_table = "ediConfirmInvoiceDetail"
        verbose_name = "Confirm Invoice Detail"
        verbose_name_plural = "Confirm Invoice Detail"
        ordering = ('seq','pds_detail_id','created_at','updated_at')
        

class PrintTAG(models.Model):
    parm_id = models.IntegerField(verbose_name="Print TAG ID")
    seq = models.IntegerField(verbose_name="Seq")
    purchase_id = models.UUIDField(verbose_name="Purchase ID")
    purchase_no = models.CharField(max_length=50,verbose_name="PO No.")
    part_no = models.CharField(max_length=255,verbose_name="Part No.")
    part_name = models.CharField(max_length=255,verbose_name="Part Name")
    part_model = models.CharField(max_length=255,verbose_name="Part Model")
    qty = models.IntegerField(verbose_name="Qty")
    unit = models.CharField(max_length=25, verbose_name="Unit")
    lot_no = models.CharField(max_length=50, verbose_name="LotNo.", blank=True, null=True)
    customer_name = models.CharField(max_length=50, verbose_name="Customer")
    print_date = models.CharField(max_length=10, verbose_name="Print Date")
    qr_code = models.CharField(max_length=255, verbose_name="QR Code", blank=True, null=True)
    is_active = models.BooleanField(verbose_name="Is Active", default=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "tmpPrintTag"
        verbose_name = "tmpPrintTag"
        verbose_name_plural = "tmpPrintTag"
        ordering = ('seq','created_at','updated_at')
        
class ReportPurchaseOrder(models.Model):
    SUP_CODE = models.CharField(max_length=255)
    SEQ = models.IntegerField()
    FCCODE = models.CharField(max_length=255)
    FCNAME = models.CharField(max_length=255)
    FDDATE = models.CharField(max_length=255,null=True, blank=True)
    FDDUEDATE = models.CharField(max_length=255,null=True, blank=True)
    FCREFNO = models.CharField(max_length=255)
    FCPARTCODE = models.CharField(max_length=255)
    FCPARTSNAME = models.CharField(max_length=255)
    FCPARTNAME = models.CharField(max_length=255)
    FNQTY = models.FloatField(null=True, blank=True)
    TOTALPRICE = models.FloatField(null=True, blank=True)
    FNBACKQTY = models.FloatField(null=True, blank=True)
    TOTALPRICE_BACKQTY = models.FloatField(null=True, blank=True)
    I_ORDER_DATE = models.CharField(max_length=255,null=True, blank=True)
    
    class Meta:
        db_table = "tmpReportPurchaseOrder"
        verbose_name = "tmpReportPurchaseOrder"
        verbose_name_plural = "tmpReportPurchaseOrder"
        ordering = ('FCCODE','SEQ','FCREFNO')