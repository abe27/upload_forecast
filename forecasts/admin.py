from datetime import datetime
from django.contrib import admin, messages
from django.contrib.auth.models import Group
from django.utils.html import format_html
from forecasts import greeter

from forecasts.models import FORECAST_ORDER_STATUS, Forecast, ForecastDetail
from upload_forecasts.models import OnMonthList, OnYearList
from members.models import ManagementUser, Supplier

# Register your models here.


class ForecastDetailInline(admin.TabularInline):
    model = ForecastDetail
    readonly_fields = (
        'seq',
        'product_id',
        'product_no',
        'product_code',
        'product_name',
        'product_group',
        'packing',
        'qty',
        'request_qty',
        'balance_qty',
        'request_status',
        'price',
        'last_updated',
        'request_status'
    )

    fields = [
        'seq',
        'product_id',
        'product_code',
        'product_name',
        'product_group',
        'request_qty',
        # 'packing',
        # 'qty',
        # 'balance_qty',
        'price',
        'request_status',
    ]

    # def updated_on(self, obj):
    #     # return obj.updated_on.strftime("%d %b %Y %H:%M:%S")
    #     return obj.updated_at.strftime("%d-%m-%Y %H:%M:%S")
    # formset = PDSDetailFormSet
    extra = 1
    max_num = 5
    can_delete = False
    can_add = False
    show_change_link = False

    def has_change_permission(self, request, obj):
        return True

    def has_add_permission(self, request, obj):
        return False
# @admin.action(description="Mark selected to Reject", permissions=["change"])


@admin.action(description="Mark selected to Reject")
def make_reject_forecast(modeladmin, request, queryset):
    # confirm_change = True
    # confirmation_fields = ['forecast_status',]
    queryset.update(forecast_status="3")

# @admin.action(description="Mark selected to Approve", permissions=["change"])


@admin.action(description="Mark selected to Approve")
def make_approve_forecast(modeladmin, request, queryset):
    ###
    data = queryset
    # isValid = False
    # for i in data:
    #     if int(i.forecast_status) > 0:
    #         isValid = True
    #         break

    # if isValid:
    #     messages.error(
    #         request, "ไม่สามารถดำเนินการตามที่ร้องขอได้เนื่องจาก สถานะของรายการไม่ถูกต้อง รบการทบทวนรายการที่เลือกใหม่ด้วย")
    #     return

    for obj in data:
        if obj.forecast_status == "0":
            greeter.create_purchase_order(request, obj.id)


class ForecastMonthFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = ("Select Month")
    # Parameter for the filter that will be used in the URL query.
    parameter_name = "on_month"

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        dte = datetime.now()
        data = OnMonthList.objects.all().values()
        docs = []
        rnd = 0
        for i in data:
            docs.append((i['id'], f"{i['name']}"))
            rnd += 1

        return docs

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        return queryset.filter(forecast_on_month_id=self.value())
# class AuthDecadeBornListFilter(ForecastMonthFilter):
#     def lookups(self, request, model_admin):
#         if request.user.is_superuser:
#             return super().lookups(request, model_admin)

#     def queryset(self, request, queryset):
#         if request.user.is_superuser:
#             return super().queryset(request, queryset)


class ForecastYearFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = ("Select Year")
    # Parameter for the filter that will be used in the URL query.
    parameter_name = "on_year"

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        dte = datetime.now()
        data = OnYearList.objects.filter(
            value__gte=int(dte.year) - 1).values()[:3]
        docs = []
        rnd = 0
        for i in data:
            docs.append((i['id'], f"{i['name']}"))
            rnd += 1

        return docs

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        return queryset.filter(forecast_on_year_id=self.value())


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

        return docs

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value() is None:
            return queryset
        
        return queryset.filter(supplier_id=self.value())


class ForecastAdmin(admin.ModelAdmin):
    change_list_template = "admin/change_list_view.html"
    change_form_template = "admin/change_form_view.html"
    inlines = [ForecastDetailInline]
    # list_display = (
    #     "forecast_no",
    #     "forecast_plan_id",
    #     # "file_forecast_id",
    #     "supplier_id",
    #     # "section_id",
    #     # "book_id",
    #     "forecast_revise_id",
    #     # "forecast_on_month_id",
    #     # "forecast_on_year_id",
    #     # "forecast_date",
    #     'part_model_id',
    #     "forecast_item",
    #     "forecast_qty",
    #     "price",
    #     # "remark",
    #     "status",
    #     "updated_on",
    # )

    # search_fields = ["forecast_no", "forecast_plan_id",
    #                  "supplier_id", 'part_model_id',]
    # list_filter = (
    #     (
    #         "forecast_date",
    #         DateTimeRangeFilterBuilder(
    #             title="Forecast Date",
    #             default_start=datetime(2020, 1, 1),
    #             default_end=datetime(2030, 1, 1),
    #         ),
    #     ),
    # )

    def get_list_filter(self, request):
        query_set = Group.objects.filter(user=request.user)
        if query_set.filter(name="Supplier").exists():
            return ["forecast_on_month_id", "forecast_on_year_id", "forecast_revise_id", ForecastSupplierFilter, 'part_model_id',]
        return [
            "forecast_on_month_id",
            "forecast_on_year_id",
            "forecast_revise_id",
            "supplier_id",
            'part_model_id',
            # "forecast_status",
        ]

    fields = [
        ('forecast_no',
        'book_id',),
        'supplier_id',
        'forecast_date',
        'forecast_item',
        'forecast_qty',
        'forecast_total_qty',
        # 'file_estimate_forecast',
        'forecast_status',
    ]

    fields = (
        'forecast_date',
        'forecast_no', 'book_id',
        'supplier_id', "forecast_item", "forecast_total_qty", "forecast_status",
    )

    readonly_fields = [
        'forecast_no',
        'book_id',
        'forecast_date',
        'forecast_item',
        'forecast_qty',
        'forecast_total_qty',
        'supplier_id',
        'forecast_status',
    ]

    list_per_page = 20

    def get_list_display(self, request):
        query_set = Group.objects.filter(user=request.user)
        if query_set.filter(name="Supplier").exists():
            return (
                "supplier_id",
                "forecast_plan_id",
                "forecast_revise_id",
                'get_model',
                "get_item",
                "get_qty",
                # "price",
                # "status",
                "updated_on",
                "download_forecast",
            )

        return (
            "forecast_no",
            "forecast_plan_id",
            "supplier_id",
            "forecast_revise_id",
            'get_model',
            "get_item",
            "get_qty",
            'total_qty',
            "forecast_download_count",
            "status",
            "updated_on",
        )

    actions = [make_approve_forecast, make_reject_forecast]

    def get_actions(self, request):
        actions = super(ForecastAdmin, self).get_actions(request)
        if request.user.is_superuser:
            return actions

        permissions = request.user.get_all_permissions()
        # {'forecasts.view_pdsheader', 'forecasts.view_pdsdetail', 'forecasts.edit_qty_price', 'forecasts.view_forecast', 'forecasts.approve_reject', 'forecasts.select_item', 'forecasts.view_forecastdetail'}
        if ('forecasts.approve_reject' in permissions) is False:
            del actions['make_approve_forecast']
            del actions['make_reject_forecast']

        return actions

    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True

        return request.user.has_perm("forecasts.is_download_report")

    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True

        return request.user.has_perm("forecasts.upload_file_forecast")

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True

        if obj != None:
            if obj.forecast_status == "0":
                return request.user.has_perm("forecasts.upload_file_estimated_forecast")

        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True

        return request.user.has_perm("forecasts.delete_forecast")

    # Set Overrides Message
    def message_user(self, request, message, level=messages.INFO, extra_tags='', fail_silently=False):
        pass

    def total_qty(self, obj):
        if obj.forecast_total_qty > 0:
            return format_html(f"<span class='text-xs badge text-bg-info'>{int(obj.forecast_total_qty):,}</span>")

        return format_html(f"<span class='text-xs badge text-bg-danger'>{obj.forecast_total_qty}</span>")
    total_qty.short_description = "Total Qty"

    def price(self, obj):
        return f'{obj.forecast_price:.2f}'

    def forecast_date_on(self, obj):
        return obj.forecast_date.strftime("%d-%m-%Y")

    def updated_on(self, obj):
        # return obj.updated_on.strftime("%d %b %Y %H:%M:%S")
        return obj.updated_at.strftime("%d-%m-%Y %H:%M:%S")

    def download_forecast(self, obj):
        txtClass = "btn-primary"
        if obj.forecast_download_count > 0:
            txtClass = "btn-secondary"
            
        return format_html(f"<a class='btn btn-sm {txtClass}' href='/forecast/export_forecast/{obj.id}' target='_blank'>Download</a>")
    download_forecast.short_description = "Download"

    def get_model(self, obj):
        return format_html(f"<span class='text-xs badge badge-success'>{obj.part_model_id}</span>")
    get_model.short_description = "Model"

    def get_qty(self, obj):
        if obj.forecast_qty > 0:
            return format_html(f"<span class='text-xs badge text-bg-secondary'>{int(obj.forecast_qty):,}</span>")

        return format_html(f"<span class='text-xs badge text-bg-danger'>{obj.forecast_qty}</span>")
    get_qty.short_description = "Qty"

    def get_item(self, obj):
        if obj.forecast_item > 0:
            return format_html(f"<span class='text-success text-bold'>{obj.forecast_item}</span>")

        return format_html(f"<span class='text-danger text-bold'>{obj.forecast_item}</span>")
    get_item.short_description = "Item"

    def forecast_download_count_on(self, obj):
        return obj.forecast_download_count
    forecast_download_count_on.short_description = "Downloaded"

    def status(self, obj):
        try:
            data = FORECAST_ORDER_STATUS[int(obj.forecast_status)]
            txtClass = ""
            if int(obj.forecast_status) == 0:
                txtClass = "badge-warning"

            elif int(obj.forecast_status) == 1:
                txtClass = "badge-success"

            elif int(obj.forecast_status) == 2:
                txtClass = "badge-primary"

            elif int(obj.forecast_status) == 3:
                txtClass = "badge-danger"

            elif int(obj.forecast_status) == 4:
                txtClass = "badge-info"

            return format_html(f"<span class='text-xs badge {txtClass}'>{data[1]}</span>")

        except:
            pass

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        if request.user.groups.filter(name='Supplier').exists() is False:
            # sup_id = []
            # usr = ManagementUser.supplier_id.through.objects.filter(managementuser_id=request.user.id)
            # for u in usr:
            #     sup_id.append(u.supplier_id)

            extra_context['wait_approve'] = Forecast.objects.filter(
                forecast_status=0).count()
            extra_context['approve_total'] = Forecast.objects.filter(
                forecast_status=1).count()
            extra_context['purchase_total'] = Forecast.objects.filter(
                forecast_status=2).count()
            extra_context['rejected_total'] = Forecast.objects.filter(
                forecast_status=3).count()
        return super().changelist_view(request, extra_context=extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        # Get object
        obj = Forecast.objects.get(id=object_id)
        # Append Variable
        extra_context['osm_data'] = obj
        extra_context['forecast_status'] = int(obj.forecast_status)
        # extra_context['forecast_revise'] = obj.edi_file_id.upload_seq
        # If Group is Planning check PR status
        isPo = False
        if request.user.groups.filter(name='Planning').exists():
            isPo = obj.ref_formula_id != None

        extra_context['send_to_po'] = isPo
        return super().change_view(request, object_id, form_url, extra_context=extra_context,)

    def get_queryset(self, request):
        greeter.request_validation(request)
        sup_id = []
        qs = super().get_queryset(request)
        if request.user.groups.filter(name='Supplier').exists():
            usr = ManagementUser.supplier_id.through.objects.filter(
                managementuser_id=request.user.id)
            for u in usr:
                sup_id.append(u.supplier_id)
                
            obj = qs.filter(forecast_status='1', supplier_id__in=sup_id, forecast_qty__gt=0)
            return obj
        
        if request.user.groups.filter(name='Purchase').exists() or request.user.groups.filter(name='Planning').exists():
            obj = qs.filter(forecast_status='0', forecast_qty__gt=0)
            return obj
        
        return qs.filter(forecast_qty__gt=0)

    # def save_model(self, request, obj, form, change):
    #     print(f"File: {bool(obj.file_estimate_forecast.name)}")
    #     if bool(obj.file_estimate_forecast.name):
    #         obj.forecast_status = "1"

    #     obj.save()
    #     return super().save_model(request, obj, form, change)
    pass

    # class Media:
    #     js = ('js/tailwind.js',)
    #     css = {
    #         'all': (
    #             'css/daisyui.css',
    #         )
    #     }


admin.site.register(Forecast, ForecastAdmin)
