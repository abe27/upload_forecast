from datetime import datetime
import os
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import Group
import requests
import xlwt

from confirm_invoices.models import ConfirmInvoiceDetail, PrintTAG, ReportPurchaseOrder
from members.models import ManagementUser
from open_pds.models import ReportPDSDetail, ReportPDSHeader
from django.conf import settings

from receives.models import ReceiveHeader

# Create your views here.
def index(request):
    return render(request, 'index.html')

def pds_reports(request, id):
    dte = datetime.now()
    rec = ReceiveHeader.objects.get(id=id)
    data = ConfirmInvoiceDetail.objects.filter(invoice_header_id=rec.confirm_invoice_id)
    head = data[0].invoice_header_id
    file_name = f"report_pds_{head.id}_{dte.strftime('%Y%m%d%H%M')}"
    rpPds = None
    try:
        ReportPDSHeader.objects.get(pds_no=head.purchase_no).delete()
    except ReportPDSHeader.DoesNotExist:
        pass
    
    rpPds = ReportPDSHeader()
    rpPds.pds_no = head.purchase_no
    deliveryDte = "-"
    if head.pds_id.pds_delivery_date:
        deliveryDte = head.pds_id.pds_delivery_date.strftime('%d-%B-%Y')
    
    ### Factory TAG ###
    usr = ManagementUser.factory_tags_id.through.objects.filter(managementuser_id=head.approve_by_id.id)
    for u in usr:
        print(u.factory_tags_id.name)
        
    rpPds.delivery_date = deliveryDte
    rpPds.sup_code = head.supplier_id.code
    rpPds.sup_name = head.supplier_id.name
    rpPds.sup_telephone = ""
    issueDte = ""
    if head.inv_date:
        issueDte = head.inv_date.strftime('%d-%B-%Y')
        
    rpPds.issue_date = issueDte
    rpPds.issue_time = ""
    rpPds.save()
    
    for r in data:
        part_code = f"{r.pds_detail_id.forecast_detail_id.product_id.no}"
        rpPdsDetail = None
        try:
            ReportPDSDetail.objects.get(pds_no=rpPds, part_code=part_code).delete()
        except:
            pass
        
        rpPdsDetail = ReportPDSDetail()
        rpPdsDetail.pds_no = rpPds
        rpPdsDetail.seq = r.seq
        rpPdsDetail.part_model = r.pds_detail_id.forecast_detail_id.import_model_by_user
        rpPdsDetail.part_code = part_code
        rpPdsDetail.part_name = f"{r.pds_detail_id.forecast_detail_id.product_id.code}:{r.pds_detail_id.forecast_detail_id.product_id.name}"
        rpPdsDetail.packing_qty = 0
        rpPdsDetail.total = float(r.total_qty)
        rpPdsDetail.is_active = True
        rpPdsDetail.save()
        
    # # import requests
    # JASPER_RESERVER
    url = f"{settings.JASPER_RESERVER}/jasperserver/rest_v2/login?j_username={settings.JASPER_USER}&j_password={settings.JASPER_PASSWORD}"
    response = requests.request("GET", url)
    
    url = f"""{settings.JASPER_RESERVER}/jasperserver/rest_v2/reports/report_forecast/print_pds.pdf?ParmID={rpPds.id}"""
    response = requests.request("GET", url, cookies=response.cookies)
    
        
    query_set = Group.objects.filter(user=request.user)
    if query_set.filter(name="Supplier").exists():
        token = os.environ.get("LINE_TOKEN")
        if type(request.user.line_notification_id) != type(None):
            token = request.user.line_notification_id.token
        
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': f'Bearer {token}'
        }
        msg = f"message=เรียนแผนก Planning/PU\nขณะนี้ทาง Supplier({request.user})\nได้ทำการโหลดเอกสาร PDS\n{head.supplier_id.name}\nเลขที่เอกสาร {head.purchase_no}\nเรียบร้อยแล้วคะ"
        requests.request("POST", "https://notify-api.line.me/api/notify", headers=headers, data=msg.encode("utf-8"))
        ### Update Download Counter
        head.is_download_count += 1
        head.save()
        
    response = HttpResponse(response, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{file_name}.pdf"'
    return response

def print_tags(request, id):
    dte = datetime.now()
    data = ConfirmInvoiceDetail.objects.filter(invoice_header_id=id)
    head = data[0].invoice_header_id
    file_name = f"print_tag_{head.id}_{dte.strftime('%Y%m%d%H%M')}"
    ### Count Tags
    parmID = PrintTAG.objects.filter(purchase_id=head.id).count() + 1
    
    for r in data:
        p = None
        try:
            p = PrintTAG.objects.get(purchase_id=head.id,part_no=r.pds_detail_id.forecast_detail_id.product_id.no)
            
        except PrintTAG.DoesNotExist:
            p = PrintTAG()
            p.purchase_id=parmID
            p.purchase_no = head.purchase_no
            p.part_no = r.pds_detail_id.forecast_detail_id.product_id.no
        
        p.parm_id = parmID
        p.seq = r.seq
        p.part_name = f"{r.pds_detail_id.forecast_detail_id.product_id.no}:{r.pds_detail_id.forecast_detail_id.product_id.name}"
        p.part_model = r.pds_detail_id.forecast_detail_id.import_model_by_user
        p.qty = r.qty
        p.unit = r.pds_detail_id.forecast_detail_id.product_id.unit_id.name
        p.lot_no = "-"
        p.customer_name = "-"
        p.print_date = dte.strftime("%d/%m/%Y")
        p.qr_code = f"{r.pds_detail_id.forecast_detail_id.product_id.no}@lotno@{r.seq}@{r.qty}"
        p.save()
        
    # JASPER_RESERVER
    url = f"{settings.JASPER_RESERVER}/jasperserver/rest_v2/login?j_username={settings.JASPER_USER}&j_password={settings.JASPER_PASSWORD}"
    response = requests.request("GET", url)
    
    print(parmID)
    url = f"""{settings.JASPER_RESERVER}/jasperserver/rest_v2/reports/report_forecast/tags_report.pdf?ParmID={parmID}"""
    response = requests.request("GET", url, cookies=response.cookies)
    
    query_set = Group.objects.filter(user=request.user)
    if query_set.filter(name="Supplier").exists():
        token = os.environ.get("LINE_TOKEN")
        if type(request.user.line_notification_id) != type(None):
            token = request.user.line_notification_id.token
        
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': f'Bearer {token}'
        }
        msg = f"message=เรียนแผนก Planning/PU\nขณะนี้ทาง Supplier({request.user})\nได้ทำการโหลดเอกสาร TAG\n{head.supplier_id.name}\nเลขที่ {head.purchase_no}\nเรียบร้อยแล้วคะ"
        try:
            requests.request("POST", "https://notify-api.line.me/api/notify", headers=headers, data=msg.encode("utf-8"))
        except:
            pass
        ### Update Download Counter
        head.is_download_count += 1
        head.save()
        
    response = HttpResponse(response, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{file_name}.pdf"'
    return response

def export_purchase(request, id):
    dte = datetime.now()
    file_name = f"export_purchase_{dte.strftime('%Y%m%d%H%M')}_{id}"
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename="{file_name}.xls"'
    
    ### Create Excel file
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Export Purchase Order')
    # Sheet header, first row
    row_num = 0
    # Create a style for the table cells with borders
    table_style = xlwt.XFStyle()

    # Set borders
    borders = xlwt.Borders()
    borders.left = xlwt.Borders.THIN
    borders.right = xlwt.Borders.THIN
    borders.top = xlwt.Borders.THIN
    borders.bottom = xlwt.Borders.THIN
    table_style.borders = borders
    
    # Set text alignment
    alignment = xlwt.Alignment()
    alignment.horz = xlwt.Alignment.HORZ_LEFT  # Right alignment
    alignment.vert = xlwt.Alignment.VERT_CENTER  # Center alignment vertically
    table_style.alignment = alignment
    
    number_format = xlwt.easyxf(num_format_str='0.00')
    combined_style = xlwt.XFStyle()

    # Copy properties from number_format
    combined_style.font = xlwt.Font()
    combined_style.font.bold = number_format.font.bold
    combined_style.font.colour_index = number_format.font.colour_index

    combined_style.pattern = xlwt.Pattern()
    combined_style.pattern.pattern = number_format.pattern.pattern
    combined_style.pattern.pattern_fore_colour = number_format.pattern.pattern_fore_colour

    # Apply table style properties
    combined_style.font.bold = table_style.font.bold
    combined_style.font.colour_index = table_style.font.colour_index
    combined_style.pattern.pattern = table_style.pattern.pattern
    combined_style.pattern.pattern_fore_colour = table_style.pattern.pattern_fore_colour

    col_widths = [2500, 10000, 3000, 4000, 4000,7000,10000, 10000,2500,3000, 3000,3000, 7000]
    columns = ["FCCODE","FCNAME","FDDATE","FDDUEDATE","FCREFNO","FCCODE","FCSNAME","FCNAME","FNQTY","TOTALPRICE","FNBACKQTY","TOTALPRICE_BACKQTY","I_ORDER_DATE",]
    
    for col_index, (header_value, width) in enumerate(zip(columns, col_widths)):
        ws.write(0, col_index, header_value,style=table_style)
        ws.col(col_index).width = width
    
    # Freeze the top row
    ws.set_panes_frozen(True)
    ws.set_remove_splits(True)
    ws.set_horz_split_pos(1)
    
    rows = ReportPurchaseOrder.objects.filter(SUP_CODE=id).values_list("FCCODE","FCNAME","FDDATE","FDDUEDATE","FCREFNO","FCPARTCODE","FCPARTSNAME","FCPARTNAME","FNQTY","TOTALPRICE","FNBACKQTY","TOTALPRICE_BACKQTY","I_ORDER_DATE")
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            val = row[col_num]
            if col_num in [8,9,10,11]:
                val = "{:,}".format(int(row[col_num]))
                
            print(f"{col_num} :: {val}")
            ws.write(row_num, col_num, val, table_style)
        
    wb.save(response)
    try:
        ReportPurchaseOrder.objects.filter(SUP_CODE=id).delete()
    except:
        pass
    #####################
    return response