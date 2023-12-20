import calendar
from datetime import datetime
import os
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import Group
from django.http import HttpResponse
from django.shortcuts import redirect
import requests
from xlutils.copy import copy    
from xlrd import open_workbook
from xlwt import XFStyle, Borders, Font, Alignment
from forecasts import greeter
from forecasts.models import Forecast, ForecastDetail

# Create your views here.
def index(request):
    greeter.request_validation(request)
    return redirect("/web/")

def approve_forecast(request, id):
    if greeter.create_purchase_order(request, id):
        messages.success(request, f"บันทึกข้อมูลเรียบร้อยแล้ว")
            
    return redirect(f"/web/forecasts/forecast/{id}/change/")

def export_forecast(request, id):
    dte = datetime.now()
    file_name = f"report_pds_{dte.strftime('%Y%m%d%H%M')}"
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename="{file_name}.xls"'
    
    book_ro = open_workbook(os.path.join(settings.BASE_DIR, 'static/file_template', 'templ_pds.xls'), formatting_info = True)
    book = copy(book_ro)  # creates a writeable copy
    sheet1 = book.get_sheet(0)  # get a first sheet
    # Create a style with desired formatting
    style = XFStyle()

    # Example: Set font properties
    font = Font()
    font.name = 'Arial'
    font.bold = True
    font.height = 14 * 20
    style.font = font

    # Example: Set alignment properties
    alignment = Alignment()
    alignment.horz = Alignment.HORZ_CENTER
    alignment.vert = Alignment.VERT_CENTER
    style.alignment = alignment


    fcHeader = Forecast.objects.get(id=id)
    sheet1.write(0,0, f"Forecast {fcHeader.forecast_plan_id} / {fcHeader.forecast_revise_id}", style)
    
    months = list(calendar.month_name)
    month_0 = fcHeader.forecast_on_month_id.value + 0
    month_1 = fcHeader.forecast_on_month_id.value + 1
    month_2 = fcHeader.forecast_on_month_id.value + 2
    month_3 = fcHeader.forecast_on_month_id.value + 3
    # print(f"month_0: {month_0} month_1: {month_1} month_2: {month_2} month_3: {month_3}")
    txt_month_0 = fcHeader.forecast_on_month_id.short_month
    txt_month_1 = ""
    txt_month_2 = ""
    txt_month_3 = ""
    if month_1 >= 13:
        n = month_1 - 12
        txt_month_1 = f"{str(months[n])}"
        txt_month_2 = f"{str(months[n + 1])}"
        txt_month_3 = f"{str(months[n + 2])}"
    else:
        y = str(dte.year)[2:]
        txt_month_1 = f"{months[month_1]}"
        if month_2 >= 13:
            n = month_2 - 12
            y = str(dte.year + 1)[2:]
            txt_month_2 = f"{str(months[n])}"
            txt_month_3 = f"{str(months[n + 1])}"
    
    styleForeHeader = XFStyle()

    # Example: Set font properties
    font = Font()
    font.name = 'Arial'
    font.bold = True
    font.height = 14 * 17
    styleForeHeader.font = font
    styleForeHeader.alignment = alignment
    
    sheet1.write(1, 10, txt_month_1, styleForeHeader)
    sheet1.write(1, 11, txt_month_2, styleForeHeader)
    sheet1.write(1, 12, txt_month_3, styleForeHeader)
    ### Append Detail
    styleBody = XFStyle()
    borders = Borders()
    borders.left = Borders.THIN
    borders.right = Borders.THIN
    borders.top = Borders.THIN
    borders.bottom = Borders.THIN
    borders.left_colour = 0x00  # Black color for the left border
    borders.right_colour = 0x00  # Black color for the right border
    borders.top_colour = 0x00  # Black color for the top border
    borders.bottom_colour = 0x00  # Black color for the bottom border
    styleBody.borders = borders

    pdsDetail = ForecastDetail.objects.filter(forecast_id=fcHeader)
    row = 2
    n = 1
    for r in pdsDetail:
        sheet1.write(row,0, n, styleBody)
        sheet1.write(row,1, r.product_id.code, styleBody)
        sheet1.write(row,2, r.product_id.no, styleBody)
        sheet1.write(row,3, r.product_id.name, styleBody)
        sheet1.write(row,4, fcHeader.supplier_id.code, styleBody)
        sheet1.write(row,5, r.import_model_by_user, styleBody)
        # print(fcHeader.forecast_revise_id.code)
        sheet1.write(row,6, r.request_qty, styleBody)
        sheet1.write(row,7, 0, styleBody)
        sheet1.write(row,8, 0, styleBody)
        sheet1.write(row,9, 0, styleBody)
        sheet1.write(row,10, r.month_1, styleBody)
        sheet1.write(row,11, r.month_2, styleBody)
        sheet1.write(row,12, r.month_3, styleBody)
        n += 1
        row += 1

    book.save(response)
    query_set = Group.objects.filter(user=request.user)
    if query_set.filter(name="Supplier").exists():
        ## Line Notification
        token = os.environ.get("LINE_TOKEN")
        if type(request.user.line_notification_id) != type(None):
            token = request.user.line_notification_id.token
        
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': f'Bearer {token}'
        }
        msg = f"message=เรียนแผนก Planning/PU\nขณะนี้ทาง Supplier ได้ทำการโหลดเอกสาร PDS\n{fcHeader.supplier_id.name} เรียบร้อยแล้วคะ"
        try:
            requests.request("POST", "https://notify-api.line.me/api/notify", headers=headers, data=msg.encode("utf-8"))
        except:
            pass
        
        if fcHeader.forecast_download_count is None:
            fcHeader.forecast_download_count = 1
        else:
            fcHeader.forecast_download_count += 1
        fcHeader.save()
    return response