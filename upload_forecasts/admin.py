import datetime
from django.contrib import admin, messages
from django.shortcuts import redirect
from books.models import Book, EDIReviseType, ReviseBook
from forecasts import greeter
from members.models import UserErrorLog

from upload_forecasts.models import OnMonthList, OnYearList, UploadForecast

# Register your models here.
# Set Overrides Message
# def message_user(self, request, message, level=messages.INFO, extra_tags='', fail_silently=False):
#     pass


class OnMonthListAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
        "is_active",
        "created_on",
        "updated_on",
    )
    pass


class OnYearListAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
        "is_active",
        "created_on",
        "updated_on",
    )
    pass


class UploadForecastAdmin(admin.ModelAdmin):
    list_display = (
        "forecast_date",
        "file_forecast",
        "forecast_month",
        "forecast_year",
        "forecast_book_id",
        "forecast_revise_id",
        "description",
        "is_generated",
        "is_active",
        "updated_on",
    )
    fields = (
        ("forecast_month", "forecast_year"),
        (
            "forecast_book_id",
            "forecast_revise_id",
        ),
        ("file_forecast",),
        "description",
    )

    # readonly_fields = ("forecast_month", "forecast_year","forecast_book_id",)
    # fieldsets = (
    #     ('Information', {
    #         'fields': (
    #             ('forecast_month', 'forecast_year'),
    #             ('forecast_book_id', 'forecast_revise_id'),)
    #     }),
    #     ('', {
    #         'fields': ('file_forecast','description')
    #     }),
    # )

    def get_changeform_initial_data(self, request):
        initData = super().get_changeform_initial_data(request)
        mydate = datetime.datetime.now()
        onMonth = int(mydate.month)
        onYear = int(mydate.year)

        ### Init Data On Month
        onMonthList = OnMonthList.objects.get(value=str(onMonth))
        initData["forecast_month"] = onMonthList

        ### Init Data On Year
        onYearList = OnYearList.objects.get(value=str(onYear))
        initData["forecast_year"] = onYearList

        ### Init Data Book
        reviseData = ReviseBook.objects.get(name="Upload EDI")
        bookData = Book.objects.get(id=reviseData.book_id.id)
        initData["forecast_book_id"] = bookData

        ### Init Data Revise
        reviseTypeData = EDIReviseType.objects.get(code="0")
        initData["forecast_revise_id"] = reviseTypeData
        return initData

    def message_user(
        self, request, message, level=messages.INFO, extra_tags="", fail_silently=False
    ):
        pass

    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True

        return request.user.has_perm("forecasts.upload_file_forecast")

    def response_add(self, request, obj, post_url_continue=None):
        return redirect("/web/forecasts/forecast/")

    def save_model(self, request, obj, form, change):
        remark = ""
        isSuccess = True
        checkDuplicate = UploadForecast.objects.filter(
            forecast_month=obj.forecast_month,
            forecast_year=obj.forecast_year,
            forecast_revise_id=obj.forecast_revise_id,
        ).first()
        if checkDuplicate is None:
            greeter.upload_file_forecast(request, obj, form, change)
            remark = "อัพโหลดข้อมูล Forecast เรียบร้อย"

        else:
            messages.error(request, "อัพโหลดข้อมูล Forecast ซ้ำ!")
            remark = "อัพโหลดข้อมูล Forecast ซ้ำ!"
            isSuccess = False

        log = UserErrorLog()
        log.user_id = request.user
        log.remark = remark
        log.is_status = isSuccess
        log.save()

    pass


admin.site.register(OnMonthList, OnMonthListAdmin)
admin.site.register(OnYearList, OnYearListAdmin)
admin.site.register(UploadForecast, UploadForecastAdmin)
