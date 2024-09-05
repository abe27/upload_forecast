from datetime import datetime
import os
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth.models import Group
from django.shortcuts import redirect, render
import requests

from open_pds.models import PDSDetail, PDSHeader, ReportPDSDetail, ReportPDSHeader

# Create your views here.
def index(request):
    return redirect("/web/")

def report_pds(request):
    return render(request, "admin/report.html")

def download_pds(request, id):
    dte = datetime.now()
    pds = PDSHeader.objects.get(id=id)
    file_name = f"report_pds_{pds.id}_{dte.strftime('%Y%m%d%H%M')}"
    # REPORTS_DIR = os.path.dirname(os.path.abspath(__file__))+'/templates/reports'
    # EXPORT_REPORTS_DIR = os.path.join(settings.BASE_DIR,'static/reports')
    # input_file = os.path.join(REPORTS_DIR, 'Invoice.jrxml')
    # output_file = os.path.join(EXPORT_REPORTS_DIR, file_name)
    
    rpPds = None
    try:
        rpPds = ReportPDSHeader.objects.get(pds_no=pds.pds_no)
        
    except ReportPDSHeader.DoesNotExist:
        rpPds = ReportPDSHeader()
        rpPds.pds_no = pds.pds_no

    rpPds.delivery_date = "-"
    if pds.pds_delivery_date:
        rpPds.delivery_date = pds.pds_delivery_date.strftime('%d-%B-%Y')
    rpPds.sup_code = pds.supplier_id.code
    rpPds.sup_name = pds.supplier_id.name
    rpPds.sup_telephone = ""
    rpPds.issue_date = pds.pds_date.strftime('%d-%B-%Y')
    rpPds.issue_time = ""
    rpPds.save()
    # ********** หมายเหตุ: หากมีข้อสงสัยประการใดกรุณาติดต่อกลับ  038-578530 ต่อ 303 **********
    
    pdsDetail = PDSDetail.objects.filter(pds_header_id=pds.id).order_by('seq')
    for r in pdsDetail:
        rpPdsDetail = None
        try:
            rpPdsDetail = ReportPDSDetail.objects.get(pds_no=rpPds, part_code=r.forecast_detail_id.product_id.code)
            
        except ReportPDSDetail.DoesNotExist:
            rpPdsDetail = ReportPDSDetail()
            rpPdsDetail.pds_no = rpPds
            rpPdsDetail.seq = r.seq
            rpPdsDetail.part_model = r.forecast_detail_id.import_model_by_user
            rpPdsDetail.part_code = r.forecast_detail_id.product_id.code
            rpPdsDetail.part_name = f"{r.forecast_detail_id.product_id.no}:{r.forecast_detail_id.product_id.name}"
            
        rpPdsDetail.packing_qty = 0
        rpPdsDetail.total = float(r.qty)
        rpPdsDetail.is_active = True
        rpPdsDetail.save()
        
    # # import requests
    # JASPER_RESERVER
    url = f"{settings.JASPER_RESERVER}/jasperserver/rest_v2/login?j_username={settings.JASPER_USER}&j_password={settings.JASPER_PASSWORD}"
    response = requests.request("GET", url)
    
    url = f"""{settings.JASPER_RESERVER}/jasperserver/rest_v2/reports/report_forecast/pds_report.pdf?ParmID={rpPds.id}"""
    response = requests.request("GET", url, cookies=response.cookies)
        
    # # print(settings.DATABASES['default']['USER'])
    # conn = {
    #     'driver': 'postgres',
    #     'username': settings.DATABASES['default']['USER'],
    #     'password': settings.DATABASES['default']['PASSWORD'],
    #     'host': settings.DATABASES['default']['HOST'],
    #     'database': settings.DATABASES['default']['NAME'],
    #     'schema': 'tempReportPDSDetail',
    #     'port': settings.DATABASES['default']['PORT'],
    #     'jdbc_driver' : 'org.postgresql.Driver'
    # }
    
    # pyreportjasper = PyReportJasper()
    # pyreportjasper.config(
    #     input_file,
    #     output_file,
    #     output_formats=["pdf"],
    #     # parameters={
    #     #     'ParmID': rpPds.id,
    #     #     'ParmDeliveryDate': str(pds.pds_delivery_date.strftime('%d-%B-%Y')),
    #     #     },
    #     # db_connection=conn,
    #     locale='th_TH',
    # )
    # pyreportjasper.process_report()
    
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
        msg = f"message=เรียนแผนก Planning/PU\nขณะนี้ทาง Supplier ได้ทำการโหลดเอกสาร PDS\n{pds.supplier_id.name} เรียบร้อยแล้วคะ"
        requests.request("POST", "https://notify-api.line.me/api/notify", headers=headers, data=msg.encode("utf-8"))
        if pds.pds_download_count is None:
            pds.pds_download_count = 1
        else:
            pds.pds_download_count += 1
        pds.save()
        
    # with open(f"{output_file}.pdf", 'rb') as f:
    #     pdf_data = f.read()
        
    response = HttpResponse(response, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{file_name}.pdf"'
    return response