import random
from django import forms
import nanoid
from django.contrib import admin, messages
from django.contrib.admin import DateFieldListFilter
from django.contrib.auth.models import Group
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.utils.html import format_html

from forecasts import greeter
from formula_vcs.models import OrderH, OrderI
from open_pds.models import PDSDetail

from .models import CONFIRM_INV_STATUS, ConfirmInvoiceDetail, ConfirmInvoiceHeader, ReportPurchaseOrder
from members.models import ManagementUser, Supplier, UserErrorLog

# Register your models here.
from django.forms.widgets import TextInput
class CustomTextInput(TextInput):
    icon = ''
    def render(self, name, value, attrs=None, renderer=None):
        if self.icon:
            final_attrs = self.build_attrs(attrs)
            return f'<div class="input-group"><span class="input-group-addon"><img src="{self.icon}" /></span>{super().render(name, value, final_attrs)}</div>'
        else:
            return super().render(name, value, attrs)


class SupplierFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = ("Select Supplier")
    # Parameter for the filter that will be used in the URL query.
    parameter_name = "supplier_id"

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        docs = []
        # if request.user.is_superuser:
        #     data = Supplier.objects.all().values("id", "code", "name")
        #     for i in data:
        #         docs.append((i['id'], f"{i['code']}-{i['name']}"))

        if request.user.groups.filter(name='Supplier').exists():
            usr = ManagementUser.supplier_id.through.objects.filter(
                managementuser_id=request.user.id)
            for u in usr:
                sup = Supplier.objects.filter(
                    id=u.supplier_id).values("id", "code", "name")
                for i in sup:
                    docs.append((i['id'], f"{i['code']}-{i['name']}"))
        else:
            data = Supplier.objects.all().values("id", "code", "name")
            for i in data:
                docs.append((i['id'], f"{i['code']}-{i['name']}"))

        # print(docs)
        return docs

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # print(self.value())
        if self.value() is None:
            return queryset
        
        return queryset.filter(supplier_id=self.value())

class BeginInvoiceDateFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = ("Start Date")
    # Parameter for the filter that will be used in the URL query.
    parameter_name = "inv_date"

    
    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return [
            ("80s", ("in the eighties")),
            ("90s", ("in the nineties")),
        ]

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value() is None:
            return queryset
        
        return queryset.filter(inv_date=self.value())

class ConfirmInvoiceDetailInline(admin.TabularInline):
    model = ConfirmInvoiceDetail
    # readonly_fields = (
    #     "invoice_header_id",
    #     "pds_detail_id",
    #     "seq",
    #     "qty",
    #     # "confirm_qty",
    #     "price",
    #     "updated_at",
    # )

    fields = (
        "seq",
        "invoice_header_id",
        "pds_detail_id",
        "qty",
        # "confirm_qty",
        "price",
        "confirm_status",
        "updated_at",
    )

    extra = 3
    max_num = 15
    can_delete = False
    can_add = False
    can_change = True
    show_change_link = False

    def get_fields(self, request, obj):
        if int(obj.inv_status) == 1:
            return (
                "seq",
                "product_code",
                "product_no",
                "product_name",
                "total",
                "price",
                "confirm_status",
                "last_update",
            )

        if request.user.has_perm("confirm_invoices.edit_qty"):
            return (
                "seq",
                "product_code",
                "product_no",
                "product_name",
                "qty",
                "confirm_qty",
                "price",
                "confirm_status",
                "last_update",
            )
        # print(obj)

        return (
            "seq",
            "product_code",
            "product_no",
            "product_name",
            "total",
            # "confirm_qty",
            "price",
            "confirm_status",
            "last_update",
        )

    def get_readonly_fields(self, request, obj):
        if int(obj.inv_status) > 0:
            return (
                "product_code",
                "product_no",
                "product_name",
                "invoice_header_id",
                "pds_detail_id",
                "seq",
                "qty",
                "confirm_qty",
                "price",
                "updated_at",
                "total",
                "last_update",
                "confirm_status",
            )
        if request.user.has_perm("confirm_invoices.edit_qty"):
            return (
                "product_code",
                "product_no",
                "product_name",
                "invoice_header_id",
                "pds_detail_id",
                "seq",
                "qty",
                # "confirm_qty",
                "price",
                "updated_at",
                "total",
                "last_update",
                "confirm_status",
            )
        # print(obj)

        return (
            "product_code",
            "product_no",
            "product_name",
            "invoice_header_id",
            "pds_detail_id",
            "seq",
            "qty",
            "confirm_qty",
            "price",
            "updated_at",
            "total",
            "last_update",
            "confirm_status",
        )

    def has_view_permission(self, request, obj):
        return True

    def has_change_permission(self, request, obj):
        # print(request.user.has_perm("open_pds.edit_qty"))
        return True

    def has_add_permission(self, request, obj):
        return False


@admin.action(description="Mark selected to Export To Excel")
def make_export_to_excel(modeladmin, request, queryset):
    obj = queryset
    seq = 1
    ids = nanoid.generate(size=10)
    for r in obj:
        # Get Details
        data = ConfirmInvoiceDetail.objects.filter(invoice_header_id=r)
        for item in data:
            inv_delivery_date = "-"
            if item.invoice_header_id.inv_delivery_date:
                inv_delivery_date = item.invoice_header_id.inv_delivery_date.strftime(
                    "%Y-%m-%d")

            rp = ReportPurchaseOrder()
            rp.SUP_CODE = ids
            rp.SEQ = seq
            rp.FCCODE = item.invoice_header_id.supplier_id.code
            rp.FCNAME = item.invoice_header_id.supplier_id.name
            rp.FDDATE = item.invoice_header_id.pds_id.pds_date.strftime(
                "%Y-%m-%d")
            rp.FDDUEDATE = inv_delivery_date
            rp.FCREFNO = item.invoice_header_id.purchase_no
            rp.FCPARTCODE = item.pds_detail_id.forecast_detail_id.product_id.code
            rp.FCPARTSNAME = item.pds_detail_id.forecast_detail_id.product_id.no
            rp.FCPARTNAME = item.pds_detail_id.forecast_detail_id.product_id.name
            rp.FNQTY = item.total_qty
            rp.TOTALPRICE = item.pds_detail_id.forecast_detail_id.product_id.price * item.total_qty
            rp.FNBACKQTY = item.total_qty
            rp.TOTALPRICE_BACKQTY = item.pds_detail_id.forecast_detail_id.product_id.price * item.total_qty
            rp.I_ORDER_DATE = item.invoice_header_id.pds_id.pds_date.strftime(
                "%Y-%m-%d %H:%M:%S")
            rp.save()
        seq += 1
        print(r)

    messages.success(request, format_html(
        f"<a href='/confirm_invoices/reports/purchase/{ids}'>กดที่ตรงนี้เพื่อดาวน์โหลดข้อมูล</a>"))

class ConfirmInvoiceHeaderAdmin(admin.ModelAdmin):
    change_list_template = "admin/change_confirm_list_view.html"
    change_form_template = "admin/change_confirm_form_view.html"
    inlines = [ConfirmInvoiceDetailInline]
    # date_hierarchy = 'inv_date'
    list_display = (
        # "pds_id",
        "purchase_no",
        "supplier_id",
        "part_model_id",
        "inv_date",
        "inv_delivery_date",
        "inv_no",
        "item",
        "qty",
        "confirm_qty",
        # "summary_price",
        # "remark",
        "get_inv_status",
        # "is_active",
        "get_updated_at",
    )

    # fields = (
    #     "purchase_no",
    #     "supplier_id",
    #     "part_model_id",
    #     "inv_date",
    #     # "inv_delivery_date",
    #     # "inv_no",
    #     "item",
    #     "qty",
    #     # "confirm_qty",
    #     "inv_status",
    # )

    list_filter = (
        "supplier_id",
        "part_model_id",
        "inv_date",
        "inv_status",
    )

    readonly_fields = (
        "purchase_no",
        "supplier_id",
        "part_model_id",
        "inv_date",
        "item",
        "qty",
        # "confirm_qty",
        "remark",
        "inv_status",
    )

    def message_user(self, request, message, level=messages.INFO, extra_tags='', fail_silently=False):
        pass

    def get_readonly_fields(self, request, obj):
        if int(obj.inv_status) > 0:
            return (
                "purchase_no",
                "supplier_id",
                "part_model_id",
                "inv_date",
                "item",
                "qty",
                "confirm_qty",
                "remark",
                "inv_status",
                "inv_delivery_date",
                "inv_no",
            )

        if request.user.has_perm("confirm_invoices.edit_qty"):
            return (
                "purchase_no",
                "supplier_id",
                "part_model_id",
                "inv_date",
                "item",
                "qty",
                # "confirm_qty",
                # "remark",
                "inv_status",
            )

        return (
            "purchase_no",
            "supplier_id",
            "part_model_id",
            "inv_date",
            "item",
            "qty",
            # "confirm_qty",
            # "remark",
            "inv_status",
        )

    def get_fields(self, request, obj):
        if request.user.has_perm("confirm_invoices.edit_qty"):
            return (
                "purchase_no",
                "supplier_id",
                "part_model_id",
                "inv_date",
                "inv_delivery_date",
                "inv_no",
                # "item",
                # "qty",
                # "confirm_qty",
                "remark",
                "inv_status",
            )

        return (
            "purchase_no",
            "supplier_id",
            "part_model_id",
            "inv_date",
            # "inv_delivery_date",
            # "inv_no",
            # "item",
            # "qty",
            # "confirm_qty",
            "remark",
            "inv_status",
        )

    def get_list_filter(self, request):
        query_set = Group.objects.filter(user=request.user)
        if query_set.filter(name="Supplier").exists():
            return [
                SupplierFilter,
                "part_model_id",
                "inv_date",
                "inv_status",
            ]

        return super().get_list_filter(request)

    def get_list_display(self, request):
        query_set = Group.objects.filter(user=request.user)
        if query_set.filter(name="Supplier").exists():
            return (
                # "pds_id",
                "purchase_no",
                "supplier_id",
                "get_part_model",
                "get_inv_date",
                "get_delivery_date",
                "inv_no",
                "item",
                "qty",
                "confirm_qty",
                # "summary_price",
                # "remark",
                "get_inv_status",
                # "is_active",
                "get_updated_at",
            )
        # download_forecast
        return (
            "purchase_no",
            "supplier_id",
            "get_part_model",
            "get_inv_date",
            "get_delivery_date",
            "inv_no",
            "item",
            "qty",
            "confirm_qty",
            "is_download_count",
            "get_inv_status",
            "get_updated_at",
        )

    # Set Overrides Message
    def message_user(self, request, message, level=messages.INFO, extra_tags='', fail_silently=False):
        pass

    def get_part_model(self, obj):
        a = ['info', 'danger', 'success', 'primary', 'secondary','warning']
        return format_html(f"<span class='badge badge-pill badge-{a[random.randrange(0, len(a) -1)]}'>{obj.part_model_id}</span>")
    get_part_model.short_description = "Model"

    def get_inv_date(self, obj):
        return format_html(f"<span class='badge badge-pill badge-warning'>{obj.inv_date.strftime('%d-%m-%Y')}</span>")
    get_inv_date.short_description = "Inv Date"

    def get_delivery_date(self, obj):
        if obj.inv_delivery_date:
            return obj.inv_delivery_date.strftime("%d-%m-%Y")
        return "-"
    get_delivery_date.short_description = "Delivery Date"

    def get_inv_status(self, obj):
        lstClass = ["badge badge-info", "text-success",
                    "badge badge-warning", "badge badge-danger"]
        return format_html(f"<strong class='{lstClass[int(obj.inv_status)]}'>{CONFIRM_INV_STATUS[int(obj.inv_status)][1]}</strong")
    get_inv_status.short_description = "Status"

    def get_updated_at(self, obj):
        return obj.updated_at.strftime("%Y-%m-%d %H:%M:%S")
    get_updated_at.short_description = "Updated At"

    # def download_forecast(self, obj):
    #     return format_html(f"<a class='btn btn-sm btn-primary' href='/forecast/export_forecast/{obj.id}' target='_blank'>Download</a>")
    # download_forecast.short_description = "Download"

    actions = [make_export_to_excel]
    # def get_actions(self, request):
    #     actions = super(ConfirmInvoiceHeaderAdmin, self).get_actions(request)
    #     if request.user.is_superuser:
    #         return actions

    #     permissions = request.user.get_all_permissions()
    #     # {'forecasts.view_pdsheader', 'forecasts.view_pdsdetail', 'forecasts.edit_qty_price', 'forecasts.view_forecast', 'forecasts.approve_reject', 'forecasts.select_item', 'forecasts.view_forecastdetail'}
    #     if ('forecasts.approve_reject' in permissions) is False:
    #         del actions['make_approve_forecast']
    #         del actions['make_reject_forecast']

    #     return actions

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        # ### Get object
        obj = ConfirmInvoiceHeader.objects.get(id=object_id)
        query_set = Group.objects.filter(user=request.user)
        extra_context['is_supplier'] = query_set.filter(
            name="Supplier").exists()
        extra_context['is_confirm'] = (int(obj.inv_status) != 1)
        if int(obj.inv_status) >= 3:
            extra_context['is_confirm'] = False
        extra_context['inv_status'] = int(obj.inv_status)
        return super().change_view(request, object_id, form_url, extra_context=extra_context,)

    def has_view_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        # if request.user.is_superuser:
        #     return True
        
        query_set = Group.objects.filter(user=request.user)
        if query_set.filter(name="Supplier").exists() is False:
            return True
        
        return request.user.has_perm("confirm_invoices.edit_qty")

    # def has_add_permission(self, request):
    #     return True

    def get_queryset(self, request):
        greeter.request_validation(request)
        return super().get_queryset(request)

    def response_change(self, request, obj):
        msgRemark = ""
        isError = True
        if '_confirm_invoice' in request.POST:
            isValid = True
            if obj.inv_delivery_date is None:
                messages.warning(request, "กรุณาระบุ Delivery Date ด้วย")
                isValid = False

            if obj.inv_no is None:
                messages.warning(request, "กรุณาระบุ Invoice No.ด้วย")
                isValid = False

            if len(obj.remark) <= 0:
                messages.warning(request, "กรุณาระบุหมายเหตุด้วยด้วย")
                isValid = False

            if isValid:
                isError = greeter.check_confirm_qty(request)
                if isError:
                    messages.warning(
                        request, f"ระบุยอด Confirm เกินกว่ายอดสั่งซื้อ")

                else:
                    if greeter.receive_invoice(request, obj):
                        messages.success(
                            request, f"Confirm Invoice {obj.inv_no} สำเร็จ")

            obj.inv_delivery_date = None
            obj.inv_no = None
            obj.remark = None
            obj.save()
            
            msgRemark = f"ยืนยัน Invoice เลขที่ {obj.inv_no}"
            
        if '_cancel_invoice' in request.POST:
            if obj.remark is None:
                messages.warning(request, "กรุณาระบุเหตุผลที่ต้องยกเลิกรายการนี้ด้วย")
                
            else:    
                obj.inv_status = "3"
                obj.pds_id.pds_status = "0"
                obj.pds_id.remark = obj.remark
                
                confirmDetail = ConfirmInvoiceDetail.objects.filter(invoice_header_id=obj)
                for r in confirmDetail:
                    r.confirm_status = "3"
                    r.remark = obj.remark
                    
                    r.pds_detail_id.remark = obj.remark
                    r.pds_detail_id.pds_detail_status = "0"
                    r.pds_detail_id.qty += r.qty
                    r.pds_detail_id.balance_qty += r.qty
                    r.pds_detail_id.save()
                    
                    ### Order PO
                    ordI = OrderI.objects.filter(FCSKID=r.pds_detail_id.ref_formula_id).first()
                    ordI.delete()
                    # ordI.FCSTEP = "C"
                    # ordI.save()
                    
                    #### Order PR
                    ordI = OrderI.objects.filter(FCSKID=r.pds_detail_id.forecast_detail_id.ref_formula_id).first()
                    ordI.FNBACKQTY += r.qty
                    ordI.save()
                    
                    r.save()
                    obj.pds_id.qty += r.qty
                
                #### Cancel ORDERH PO
                ordH = OrderH.objects.filter(FCSKID=obj.pds_id.ref_formula_id).first()
                ordH.delete()
                # ordH.FCSTEP = "C"
                # ordH.save()
                
                # #### UPDATE ORDERH PR
                # ordH = OrderH.objects.filter(FCSKID=obj.pds_id.forecast_id.ref_formula_id).first()
                # ordH.FCSTEP = "C"
                # ordH.save()
                # print(len(confirmDetail))
                
                item = PDSDetail.objects.filter(pds_header_id=obj.pds_id).count()
                obj.pds_id.pds_no = obj.pds_id.forecast_id.forecast_no
                obj.pds_id.item = item
                obj.pds_id.save()
                obj.save()
                
                msgRemark = f"ยกเลิกรายการ {obj.purchase_no}"
            
                messages.success(request, f"ยกเลิกรายการนี้ {obj.purchase_no} แล้ว")
                
        rp = UserErrorLog()
        rp.user_id = request.user
        rp.remark = msgRemark
        rp.is_status = isError
        rp.save()

        return super().response_change(request, obj)
    pass


admin.site.register(ConfirmInvoiceHeader, ConfirmInvoiceHeaderAdmin)
