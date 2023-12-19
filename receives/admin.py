import random
from django.contrib import admin
from django.contrib.auth.models import Group
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.utils.html import format_html

from forecasts import greeter
from members.models import UserErrorLog
from .models import RECEIVE_INV_STATUS, ReceiveHeader, ReceiveDetail

# Register your models here.

class ReceiveDetailInline(admin.TabularInline):
    model = ReceiveDetail
    readonly_fields = (
        "confirm_detail_id",
        "part_code",
        "part_no",
        "part_name",
        "seq",
        "qty",
        "summary_price",
        "receive_status",
    )
    
    fields = (
        "seq",
        "part_code",
        "part_no",
        "part_name",
        "qty",
        "summary_price",
        "receive_status",
    )
    
    extra = 3
    max_num = 15
    can_delete = False
    can_add = False
    can_change = True
    show_change_link = False
    
    def has_view_permission(self, request, obj):
        return True
    
    def has_add_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    def has_change_permission(self, request, obj=None):
        return True
    
class ReceiveHeaderAdmin(admin.ModelAdmin):
    change_form_template = "admin/change_receive_form_view.html"
    inlines = [ReceiveDetailInline]
    list_display = (
        "inv_no",
        "get_delivery_date",
        "supplier_id",
        "get_tag_model",
        # "purchase_no",
        "show_po_detail",
        "item",
        "qty",
        "summary_price",
        "status",
        "updated_at",
    )
    
    fields = (
        "inv_no",
        "inv_delivery_date",
        "supplier_id",
        "part_model_id",
        "purchase_no",
        # "item",
        # "qty",
        # "summary_price",
        "remark",
        "receive_status",
    )
    
    readonly_fields = fields
    
    def show_po_detail(self, obj):
        return format_html(f'<a target="blank" href="/web/confirm_invoices/confirminvoiceheader/{obj.confirm_invoice_id}/change/">{obj.purchase_no}</a>')
    show_po_detail.short_description = "PDS No."
    
    def get_delivery_date(self, obj):
        return obj.inv_delivery_date.strftime("%d-%m-%Y")
    get_delivery_date.short_description = "Delivery Date"
    
    def get_tag_model(self, obj):
        a = ['info', 'success', 'danger', 'warning', 'secondary']
        return format_html(f"<span class='badge badge-{a[random.randint(0, len(a) - 1)]}'>{obj.part_model_id}</span>")
    get_tag_model.short_description = "Model"
    
    
    def status(self, obj):
        try:
            data = RECEIVE_INV_STATUS[int(obj.receive_status)]
            txtClass = ""
            if int(obj.receive_status) == 0:
                txtClass = "badge-info"

            elif int(obj.receive_status) == 1:
                txtClass = "badge-success"

            elif int(obj.receive_status) == 2:
                txtClass = "badge-danger"

            elif int(obj.receive_status) == 3:
                txtClass = "badge-danger"

            elif int(obj.receive_status) == 4:
                txtClass = "badge-info"

            return format_html(f"<span class='font-weight-bold badge {txtClass}'>{data[1]}</span>")
        
        except:
            pass
        return format_html(f"<span class='text-bold'>-</span>")
    
    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        # ### Get object
        query_set = Group.objects.filter(user=request.user)
        extra_context['is_supplier'] = query_set.filter(
            name="Supplier").exists()
        rec = ReceiveHeader.objects.get(id=object_id)
        extra_context['object_id'] = object_id
        extra_context['receive_status'] = int(rec.receive_status)
        return super().change_view(request, object_id, form_url, extra_context=extra_context,)
    
    def get_queryset(self, request):
        greeter.request_validation(request)
        return super().get_queryset(request)
    
    def response_change(self, request, obj):
        if '_cancel_invoice' in request.POST:
            obj.receive_status = "2"
            recDetail = ReceiveDetail.objects.filter(receive_header_id=obj)
            sumQty = 0
            for i in recDetail:
                i.receive_status = "2"
                i.confirm_detail_id.qty += i.qty
                i.confirm_detail_id.confirm_status = "0"
                i.confirm_detail_id.save()
                i.save()
                sumQty += i.qty
            
            obj.confirm_invoice_id.inv_status = "0"   
            obj.confirm_invoice_id.qty = sumQty
            obj.confirm_invoice_id.save()
            obj.save()
            
            rp = UserErrorLog()
            rp.user_id = request.user
            rp.remark = f"ยกเลิกรายการ {obj.receive_no}"
            rp.is_status = True
            rp.save()
            
        return super().response_change(request, obj)
    pass
admin.site.register(ReceiveHeader, ReceiveHeaderAdmin)
