from random import randint
from django import forms
from django.contrib import admin, messages
from django.contrib.auth.models import Group
from django.utils.html import format_html

from forecasts import greeter
from members.models import ManagementUser, Supplier, UserErrorLog
from .models import FORECAST_PDS_STATUS, PDSDetail, PDSHeader

# Register your models here.
class ForecastSupplierFilter(admin.SimpleListFilter):
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
        if request.user.groups.filter(name='Supplier').exists():
            usr = ManagementUser.supplier_id.through.objects.filter(managementuser_id=request.user.id)
            for u in usr:
                sup = Supplier.objects.filter(id=u.supplier_id).values("id", "code", "name")
                for i in sup:
                    docs.append((i['id'], f"{i['code']}-{i['name']}"))
        else:
            data = Supplier.objects.all().values("id", "code", "name")
            for i in data:
                docs.append((i['id'], f"{i['code']}-{i['name']}"))
            
        return docs

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # print(self.value())
        return queryset.filter(supplier_id=self.value())


class PDSDetailForm(forms.ModelForm):
    is_select = forms.BooleanField(label="Select", required=False)

    class Meta:
        model = PDSDetail
        fields = ['is_select']


class PDSDetailInlineAdmin(admin.TabularInline):
    form = PDSDetailForm
    model = PDSDetail
    list_readonly_fields = (
        'forecast_detail_id',
        'product_code',
        'product_no',
        'product_name',
        'get_model',
        'seq',
        # 'qty',
        'balance_qty',
        'price',
        'is_active',
        'pds_detail_status'
    )

    extra = 3
    max_num = 5
    can_delete = False
    can_add = False
    can_change = True
    show_change_link = False

    def get_readonly_fields(self, request, obj=None):
        if request.user.has_perm("open_pds.edit_qty"):
            if int(obj.pds_status) == 2:
                return self.list_readonly_fields + ('qty','is_select',)
            
            return self.list_readonly_fields
        
        return self.list_readonly_fields + ('is_select',)

    def get_fields(self, request, obj):
        if request.user.has_perm("open_pds.edit_qty"):
            return [
                'is_select',
                'seq',
                'product_code',
                'product_no',
                'product_name',
                'get_model',
                'qty',
                'balance_qty',
                'price',
                'pds_detail_status',
            ]

        query_set = Group.objects.filter(user=request.user)
        if query_set.filter(name="Purchase").exists():
            return [
                # 'is_select',
                'seq',
                'product_code',
                'product_no',
                'product_name',
                'get_model',
                'qty',
                'balance_qty',
                'price',
                'pds_detail_status'
            ]

        return [
            # 'is_select',
            'seq',
            'product_code',
            'product_no',
            'product_name',
            'get_model',
            'qty',
            # 'balance_qty',
            'price',
            'pds_detail_status'
        ]

    def has_change_permission(self, request, obj):
        # print(request.user.has_perm("open_pds.edit_qty"))
        return True

    def has_add_permission(self, request, obj):
        return False

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        obj = qs.filter(balance_qty__gt=0)
        return obj

    pass


class PDSHeaderAdmin(admin.ModelAdmin):
    change_form_template = "admin/open_pds_form_view.html"
    change_list_template = "admin/open_pds_list_view.html"
    inlines = [PDSDetailInlineAdmin]
    
    def get_fields(self, request, obj=None):
        query_set = Group.objects.filter(user=request.user)
        if query_set.filter(name="Supplier").exists():
            return [
                # "pds_date",
                # "forecast_id",
                "pds_no",
                "pds_date",
                'part_model_id',
                "item",
                "qty",
                'pds_delivery_date',
                # "summary_price",
                "remark",
                "pds_status",
            ]
        
        if query_set.filter(name="Purchase").exists():
            return [
                "pds_date",
                "forecast_id",
                'part_model_id',
                # "pds_no",
                "item",
                "qty",
                'pds_delivery_date',
                # "summary_price",
                "remark",
                "pds_status",
            ]
        
        return [
            "pds_no",
            'pds_delivery_date',
            "pds_date",
            "forecast_id",
            'part_model_id',
            "item",
            "qty",
            "remark",
            "pds_status",
        ]
    
    list_readonly_fields = [
        "forecast_id",
        "pds_date",
        "pds_no",
        "item",
        "qty",
        'balance_qty',
        "summary_price",
        "pds_status",
        "ref_formula_id",
        'part_model_id',
        "is_active",
        "pds_status",
    ]
    
    def get_readonly_fields(self, request, obj=None):
        # print(obj.pds_status == 2)
        if int(obj.pds_status) == 0:
            return [
                    "forecast_id",
                    "pds_date",
                    "pds_no",
                    "item",
                    "qty",
                    'balance_qty',
                    "summary_price",
                    "pds_status",
                    "ref_formula_id",
                    'part_model_id',
                    "is_active",
                ]
        if int(obj.pds_status) == 2:
            self.list_readonly_fields += ['pds_delivery_date', 'remark',]
            
        return self.list_readonly_fields
    
    # list_filter = ["forecast_plan_id", "supplier_id", "pds_status"]
    def get_list_filter(self, request):
        query_set = Group.objects.filter(user=request.user)
        if query_set.filter(name="Supplier").exists():
            return ["forecast_plan_id", ForecastSupplierFilter, 'part_model_id',"pds_status"]
        
        return ["forecast_plan_id", "supplier_id", 'part_model_id',"pds_status"]
    
    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        
        return request.user.has_perm("open_pds.is_download_report")
    
    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        
        return request.user.has_perm("open_pds.create_purchase_order")
    
    # actions = [make_export_to_excel]
    # actions = [mark_as_po]
    # def get_actions(self, request):
    #     actions = super().get_actions(request)
    #     permissions = request.user.get_all_permissions()
    #     # print(permissions)
    #     if ('forecasts.create_purchase_order' in permissions) is False:
    #         del actions['mark_as_po']
        
    #     return actions
    
    def get_pds_date(self, obj):
        return obj.pds_date.strftime("%d-%m-%Y")
    get_pds_date.short_description = "PDS Date"
    
    def get_last_update_date(self, obj):
        return obj.updated_at.strftime("%d-%m-%Y %H:%M:%S")
    get_last_update_date.short_description = "Update At"
    
    def get_forecast_id(self, obj):
        return obj.forecast_id
    get_forecast_id.short_description = "Purchase No."
    def get_supplier_name(self, obj):
        return obj.forecast_id.supplier_id
    get_supplier_name.short_description = "Supplier Name"
    
    def get_part_model(self, obj):
        a = ['info','primary','secondary','success','danger','warning','dark','light']
        return format_html(f'<span class="badge badge-{a[randint(0, len(a) - 1)]}">{obj.part_model_id}</span>')
    get_part_model.short_description = "Model"
    
    def download_pds(self, obj):
        if int(str(obj.pds_status)) >= 1:
            return format_html(f"<a class='btn btn-sm btn-primary' href='/open_pds/download_pds/{obj.id}' target='_blank'>Download</a>")
        return "-"
    download_pds.short_description = "Download"
    
    def get_pds_delivery_date(self, obj):
        if obj.pds_delivery_date is None:
            return "-"
        
        dlDte = int(f"{obj.forecast_id.forecast_on_year_id.value}{obj.forecast_id.forecast_on_month_id.value}")
        if dlDte != int(obj.pds_delivery_date.strftime("%Y%m")):
            return format_html(f'<span class="badge badge-danger">{obj.pds_delivery_date.strftime("%d-%m-%Y")}</span>')
        
        return format_html(f'<span class="text-success">{obj.pds_delivery_date.strftime("%d-%m-%Y")}</span>')
    get_pds_delivery_date.short_description = "Delivery Date"
    
    def get_qty(self, obj):
        # if obj.qty <= 0:
        #     return obj.total_qty
        return obj.qty
    get_qty.short_description = "Qty"
    
    def get_item(self, obj):
        # if obj.item <= 0:
        #     return obj.total_item
        return obj.item
    get_item.short_description = "Item"
        
    def check_data_status(self, obj):
        if int(obj.pds_status) >= 1:
            return obj.pds_no
        return obj.forecast_id
    
    def status(self, obj):
        try:
            data = FORECAST_PDS_STATUS[int(obj.pds_status)]
            txtClass = ""
            if int(obj.pds_status) == 0:
                txtClass = "badge-info"

            elif int(obj.pds_status) == 1:
                txtClass = "badge-warning"

            elif int(obj.pds_status) == 2:
                txtClass = "badge-success"

            elif int(obj.pds_status) == 3:
                txtClass = "badge-danger"

            elif int(obj.pds_status) == 4:
                txtClass = "badge-warning"

            return format_html(f"<span class='text-xs badge {txtClass}'>{data[1]}</span>")
        
        except:
            pass
        return format_html(f"<span class='text-bold'>-</span>")
    
    
    def get_list_display(self, request):
        query_set = Group.objects.filter(user=request.user)
        if query_set.filter(name="Supplier").exists():
            return [
                "get_supplier_name",
                "get_pds_date",
                "forecast_plan_id",
                "pds_revise_id",
                'get_part_model',
                "get_item",
                "get_qty",
                "get_pds_delivery_date",
                "remark",
                "get_last_update_date",
                "download_pds"
            ]

        return [
            "check_data_status",
            "get_pds_date",
            "pds_revise_id",
            "get_supplier_name",
            'get_part_model',
            "get_item",
            "get_qty",
            # 'balance_qty',
            "get_pds_delivery_date",
            "remark",
            "pds_download_count",
            "status",
            "get_last_update_date",
        ]
    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        ### Get object
        obj = PDSHeader.objects.get(id=object_id)
        ### Append Variable
        extra_context['osm_data'] = obj
        if obj.pds_status is None:
            extra_context['pds_status'] = 0
        else:
            extra_context['pds_status'] = int(obj.pds_status)
            if int(obj.pds_status) == 1:
                extra_context['pds_status'] = 0
            
        ### If Group is Planning check PR status
        isPo = False
        if request.user.groups.filter(name='Planning').exists():
            isPo = obj.ref_formula_id != None
    
        extra_context['send_to_po'] = isPo
        return super().change_view(request, object_id, form_url, extra_context=extra_context,)
    
    # Set Overrides Message
    def message_user(self, request, message, level=messages.INFO, extra_tags='', fail_silently=False):
        pass
    
    def response_change(self, request, obj):
        isSuccess = True
        msg = "จัดการข้อมูล PDS"
        if "_move_to_po" in request.POST:
            if obj.pds_delivery_date is None:
                isSuccess = False
                msg = "ไม่ระบุ Delivery Date"
                messages.error(request,"กรุณาระบุ Delivery Date ด้วย")
                
            else:
                if int(obj.pds_delivery_date.strftime("%Y%m")) == int(f"{obj.forecast_id.forecast_on_year_id.value}{obj.forecast_id.forecast_on_month_id.value}"):
                    isSuccess= greeter.create_purchase_order(request, obj.id, "PO", "002")
                    if isSuccess:
                        msg = f"ทำการเปิด PDS หมายเลข {obj.pds_no}"
                        messages.success(request, f"บันทึกข้อมูลเรียบร้อยแล้ว")
                else:
                    isSuccess = False
                    msg = f"ระบุวันที่ Delivery Date ไม่ตรงกับรายการ Forecast"
                    messages.error(request, f"กรุณาเลือกวันที่จัดส่งให้ถูกต้องด้วย")
                        
        elif "_cancel_po" in request.POST:
            isSuccess = True
            msg = f"ทำการยกเลิก PDS หมายเลข {obj.pds_no}"
            messages.success(request, f"ยกเลิกรายการ {obj.pds_no} นี้แล้วเรียบร้อยแล้ว")
        
        log = UserErrorLog()
        log.user_id = request.user
        log.remark = msg
        log.is_status = isSuccess
        log.save()
        return super().response_change(request, obj)
    
    def get_queryset(self, request):
        greeter.request_validation(request)
        sup_id = []
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs.filter(qty__gt=0)
        
        usr = ManagementUser.supplier_id.through.objects.filter(managementuser_id=request.user.id)
        for u in usr:
            sup_id.append(u.supplier_id)
        
        if request.user.groups.filter(name='Supplier').exists():
            obj = qs.filter(supplier_id__in=sup_id, qty__gt=0)
            return obj
        return qs.filter(qty__gt=0)
    
    class Meta:
        css = {
            'all': (
                'css/input.css',
            )
        }

    
    pass


admin.site.register(PDSHeader, PDSHeaderAdmin)
