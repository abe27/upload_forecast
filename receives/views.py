from datetime import datetime
import os
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth.models import Group
from django.contrib import messages
from django.shortcuts import redirect
import requests

from confirm_invoices.models import PrintTAG
from receives.models import ReceiveDetail

# Create your views here.
def print_tags(request, id):
    try:
        dte = datetime.now()
        data = ReceiveDetail.objects.filter(receive_header_id=id, qty__gt=0)
        head = data[0].receive_header_id
        file_name = f"print_tag_{head.id}_{dte.strftime('%Y%m%d%H%M')}"
        # print(head.id)
        try:
            PrintTAG.objects.filter(purchase_id=head.id).delete()
        except:
            pass
        
        ### Count Tags
        parmID = PrintTAG.objects.filter(purchase_id=head.id).count() + 1
        seq = 0
        ### หาจำนวน TAG
        for obj in data:
            r = obj.confirm_detail_id
            stdPack = int(r.pds_detail_id.forecast_detail_id.product_id.std_pack)
            
            if stdPack <= 0:
                messages.error(request, f"กรุณาแจ้ง Planning ให้ระบุ Standard Packing ขอ {r.pds_detail_id.forecast_detail_id.product_id.no} ด้วย")
                return redirect(request.META.get('HTTP_REFERER'))
            # print(f"PARTNO: {part_no} QTY: {obj.qty} STD: {stdPack}")
            bQty = int(obj.qty/stdPack)
            balQty = int(obj.qty - int(bQty)*stdPack)
            # print(f"Start QTY: {bQty}")
            for n in range(bQty):
                seq += 1
                qrCode = f"{r.pds_detail_id.forecast_detail_id.product_id.no}@lotno@{seq}@{stdPack}"
                # print(f"{n}. {stdPack} QRCode: {qrCode}")
                p = None
                try:
                    p = PrintTAG.objects.get(purchase_id=head.id,qr_code=qrCode)
                    
                except PrintTAG.DoesNotExist:
                    p = PrintTAG()
                    p.purchase_id=head.id
                    p.purchase_no = head.purchase_no
                    p.part_no = r.pds_detail_id.forecast_detail_id.product_id.no
                    
                p.parm_id = parmID
                p.seq = seq
                p.part_name = f"{r.pds_detail_id.forecast_detail_id.product_id.no}:{r.pds_detail_id.forecast_detail_id.product_id.name}"
                p.part_model = r.pds_detail_id.forecast_detail_id.import_model_by_user
                p.qty = int(stdPack)
                p.unit = r.pds_detail_id.forecast_detail_id.product_id.unit_id.name
                p.lot_no = "-"
                p.customer_name = "-"
                p.print_date = dte.strftime("%d/%m/%Y")
                p.qr_code = qrCode
                p.save()
            
            if balQty > 0:
                seq += 1
                qrCode = f"{r.pds_detail_id.forecast_detail_id.product_id.no}@lotno@{seq}@{balQty}"
                # print(f"{seq}. {balQty} QRCode: {qrCode}")
                p = None
                try:
                    p = PrintTAG.objects.get(purchase_id=head.id,qr_code=qrCode)
                    
                except PrintTAG.DoesNotExist:
                    p = PrintTAG()
                    p.purchase_id=head.id
                    p.purchase_no = head.purchase_no
                    p.part_no = r.pds_detail_id.forecast_detail_id.product_id.no
                    
                p.parm_id = parmID
                p.seq = seq
                p.part_name = f"{r.pds_detail_id.forecast_detail_id.product_id.no}:{r.pds_detail_id.forecast_detail_id.product_id.name}"
                p.part_model = r.pds_detail_id.forecast_detail_id.import_model_by_user
                p.qty = int(balQty)
                p.unit = r.pds_detail_id.forecast_detail_id.product_id.unit_id.name
                p.lot_no = "-"
                p.customer_name = "-"
                p.print_date = dte.strftime("%d/%m/%Y")
                p.qr_code = qrCode
                p.save()
        
        # print(f"Total SEQ: {seq}")
        
        # for obj in data:
        #     r = obj.confirm_detail_id
        #     stdPack = r.pds_detail_id.forecast_detail_id.product_id.std_pack
        #     p = None
        #     try:
        #         p = PrintTAG.objects.get(purchase_id=head.id,part_no=r.pds_detail_id.forecast_detail_id.product_id.no)
                
        #     except PrintTAG.DoesNotExist:
        #         p = PrintTAG()
        #         p.purchase_id=parmID
        #         p.purchase_no = head.purchase_no
        #         p.part_no = r.pds_detail_id.forecast_detail_id.product_id.no
            
        #     # print(stdPack)
        #     if stdPack <= 0:
        #         messages.error(request, f"กรุณาแจ้ง Planning ให้ระบุ Standard Packing ขอ {r.pds_detail_id.forecast_detail_id.product_id.no} ด้วย")
        #         return redirect(request.META.get('HTTP_REFERER'))
        #     bQty = obj.qty/stdPack
        #     print(obj.qty - int(bQty)*stdPack)
        #     p.parm_id = parmID
        #     p.seq = obj.seq
        #     p.part_name = f"{r.pds_detail_id.forecast_detail_id.product_id.no}:{r.pds_detail_id.forecast_detail_id.product_id.name}"
        #     p.part_model = r.pds_detail_id.forecast_detail_id.import_model_by_user
        #     p.qty = int(bQty)
        #     p.unit = r.pds_detail_id.forecast_detail_id.product_id.unit_id.name
        #     p.lot_no = "-"
        #     p.customer_name = "-"
        #     p.print_date = dte.strftime("%d/%m/%Y")
        #     p.qr_code = f"{r.pds_detail_id.forecast_detail_id.product_id.no}@lotno@{r.seq}@{r.qty}"
        #     p.save()
            
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
    
    except Exception as e:
        messages.error(request, f"เกิดข้อผิดพลาดในการเชื่อมต่อ Report Server")
        return redirect(request.META.get('HTTP_REFERER'))