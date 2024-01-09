from datetime import datetime
import os
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth.models import Group
import requests

from confirm_invoices.models import PrintTAG
from receives.models import ReceiveDetail

# Create your views here.
def print_tags(request, id):
    dte = datetime.now()
    data = ReceiveDetail.objects.filter(receive_header_id=id, qty__gt=0)
    head = data[0].receive_header_id
    file_name = f"print_tag_{head.id}_{dte.strftime('%Y%m%d%H%M')}"
    ### Count Tags
    parmID = PrintTAG.objects.filter(purchase_id=head.id).count() + 1
    for obj in data:
        r = obj.confirm_detail_id
        p = None
        try:
            p = PrintTAG.objects.get(purchase_id=head.id,part_no=r.pds_detail_id.forecast_detail_id.product_id.no)
            
        except PrintTAG.DoesNotExist:
            p = PrintTAG()
            p.purchase_id=parmID
            p.purchase_no = head.purchase_no
            p.part_no = r.pds_detail_id.forecast_detail_id.product_id.no
        
        p.parm_id = parmID
        p.seq = obj.seq
        p.part_name = f"{r.pds_detail_id.forecast_detail_id.product_id.no}:{r.pds_detail_id.forecast_detail_id.product_id.name}"
        p.part_model = r.pds_detail_id.forecast_detail_id.import_model_by_user
        p.qty = obj.qty
        p.unit = r.pds_detail_id.forecast_detail_id.product_id.unit_id.name
        p.lot_no = "-"
        p.customer_name = "-"
        p.print_date = dte.strftime("%d/%m/%Y")
        p.qr_code = f"{r.pds_detail_id.forecast_detail_id.product_id.no}@lotno@{r.seq}@{r.qty}"
        p.save()
        
    # JASPER_RESERVER
    url = f"{settings.JASPER_RESERVER}/jasperserver/rest_v2/login?j_username={settings.JASPER_USER}&j_password={settings.JASPER_PASSWORD}"
    response = requests.request("GET", url)
    
    url = f"""{settings.JASPER_RESERVER}/jasperserver/rest_v2/reports/report_forecast/print_tags.pdf?ParmID={parmID}"""
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