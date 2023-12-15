import uuid
from django.db import models
from confirm_invoices.models import ConfirmInvoiceDetail, ConfirmInvoiceHeader
from products.models import ProductGroup

from members.models import ManagementUser, Supplier

RECEIVE_INV_STATUS = [
    ("0", "รอรับ"),
    ("1", "รับแล้ว"),
    ('2', 'ยกเลิกจัดส่ง')
]

# Create your models here.
class ReceiveHeader(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, verbose_name="PRIMARY KEY", default=uuid.uuid4)
    receive_by_id = models.ForeignKey(ManagementUser, verbose_name="Receive By ID", blank=True, null=True, on_delete=models.SET_NULL)
    confirm_invoice_id = models.ForeignKey(ConfirmInvoiceHeader, verbose_name="PO No.", blank=False, null=False, on_delete=models.CASCADE, editable=False)
    supplier_id = models.ForeignKey(Supplier, verbose_name="Supplier ID", blank=True, null=True, on_delete=models.SET_NULL)
    part_model_id = models.ForeignKey(ProductGroup, verbose_name="Model ID", on_delete=models.SET_NULL, null=True, blank=True)
    purchase_no = models.CharField(max_length=15,verbose_name="PO No.", blank=True, null=True)
    receive_no = models.CharField(max_length=15,verbose_name="Receive No.", blank=True, null=True)
    receive_date = models.DateField(verbose_name="Invoice Date", blank=True, null=True)
    inv_delivery_date = models.DateField(verbose_name="Delivery Date", blank=True, null=True)
    inv_no = models.CharField(max_length=15,verbose_name="Invoice No.", blank=True, null=True)
    item = models.IntegerField(verbose_name="Item")
    qty = models.IntegerField(verbose_name="Qty")
    summary_price = models.FloatField(verbose_name="Summary Price", blank=True, null=True, default="0")
    remark = models.TextField(verbose_name="Remark", blank=True, null=True)
    receive_status = models.CharField(max_length=1, choices=RECEIVE_INV_STATUS,verbose_name="Receive Status", blank=True, null=True, default="0")
    ref_formula_id = models.CharField(max_length=8, blank=True, null=True, verbose_name="Formula ID")
    is_download_count = models.IntegerField(verbose_name="Download Count", blank=True, null=True, default="0")
    is_active = models.BooleanField(verbose_name="Is Active", default=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.inv_no
    
    class Meta:
        db_table = "ediReceiveHeader"
        verbose_name = "Receive"
        verbose_name_plural = "EDI Confirm Invoice"
        
class ReceiveDetail(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, verbose_name="PRIMARY KEY", default=uuid.uuid4)
    receive_header_id = models.ForeignKey(ReceiveHeader, verbose_name="Receive ID", blank=False, null=False, on_delete=models.CASCADE, editable=False)
    confirm_detail_id = models.ForeignKey(ConfirmInvoiceDetail, verbose_name="Confirm Detail", on_delete=models.CASCADE)
    seq = models.IntegerField(verbose_name="Seq")
    qty = models.IntegerField(verbose_name="Qty")
    summary_price = models.FloatField(verbose_name="Summary Price", blank=True, null=True, default="0")
    remark = models.TextField(verbose_name="Remark", blank=True, null=True)
    receive_status = models.CharField(max_length=1, choices=RECEIVE_INV_STATUS,verbose_name="Receive Status", blank=True, null=True, default="0")
    ref_formula_id = models.CharField(max_length=8, blank=True, null=True, verbose_name="Formula ID")
    is_active = models.BooleanField(verbose_name="Is Active", default=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def part_code(self):
        return self.confirm_detail_id.pds_detail_id.forecast_detail_id.product_id.code
    
    def part_no(self):
        return self.confirm_detail_id.pds_detail_id.forecast_detail_id.product_id.no
    
    def part_name(self):
        return self.confirm_detail_id.pds_detail_id.forecast_detail_id.product_id.name
    
    class Meta:
        db_table = "ediReceiveDetail"
        verbose_name = "Receive Detail"
        verbose_name_plural = "Receive Detail"
        ordering = ['seq',]