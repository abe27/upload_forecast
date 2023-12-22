from datetime import datetime
from django.contrib import messages
from django.contrib.auth.models import Group
from django.utils.html import format_html
import os
from django.conf import settings
import nanoid
import numpy as np
import pandas as pd
# from confirm_invoice.models import ConfirmInvoiceDetail, ConfirmInvoiceHeader
# from reportlab.lib.pagesizes import letter
# from reportlab.lib.styles import getSampleStyleSheet
# from reportlab.lib.units import mm, inch
# from reportlab.pdfgen import canvas
# from reportlab.platypus import Image, Paragraph, Table, Frame
# from reportlab.lib import colors
from books.models import Book, ReviseBook
from confirm_invoices.models import ConfirmInvoiceDetail, ConfirmInvoiceHeader
from open_pds.models import CheckLastPurchaseRunning, PDSDetail, PDSHeader
from products.models import Product, ProductGroup
from receives.models import ReceiveDetail, ReceiveHeader
from forecasts.models import Forecast
from forecasts import apps as forecast_apps
from open_pds import apps as open_pds_apps
from open_pds.models import PDSHeader
from receives import apps as receive_apps
from receives.models import ReceiveHeader
from confirm_invoices import apps as confirm_invoice_apps
from confirm_invoices.models import ConfirmInvoiceHeader

from upload_forecasts.models import ForecastErrorLogs, OnMonthList, OnYearList
from members.models import PlanningForecast, Section, Supplier, UserErrorLog

# styles = getSampleStyleSheet()
# styleN = styles['Normal']
# style = getSampleStyleSheet()
# styleH = styles['Heading1']


import requests

from forecasts.models import Forecast, ForecastDetail
# from open_pds.models import PDSDetail, PDSHeader
from formula_vcs.models import BOOK, COOR, CORP, DEPT, EMPLOYEE, PROD, SECT, UM, NoteCut, OrderH, OrderI

def create_purchase_order(request, id, prefixRef="PR", bookGroup="0002"):
    dte = datetime.now()
    ordH = None
    txtMsg =""
    # try:
    ## Line Notification
    token = os.environ.get("LINE_TOKEN")
    if type(request.user.line_notification_id) != type(None):
        token = request.user.line_notification_id.token
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': f'Bearer {token}'
    }
    
    ### Get Formula Master Data
    formulaUser = "TEST"
    if type(request.user.formula_user_id) != type(None):
        formulaUser = request.user.formula_user_id.code
        
    formulaDepartment = "-"
    if type(request.user.department_id)!= type(None):
        formulaDepartment = request.user.department_id.code
        
    formulaSect = "-"
    if type(request.user.section_id)!= type(None):
        formulaSect = request.user.section_id.code
    
    emp = EMPLOYEE.objects.filter(FCCODE=formulaUser).first()
    dept = DEPT.objects.filter(FCCODE=formulaDepartment).first()
    sect = SECT.objects.filter(FCCODE=formulaSect).first()
    corp = CORP.objects.all().first()
    ordBook = BOOK.objects.filter(FCREFTYPE=prefixRef, FCCODE=bookGroup).first()
    
    fcStep = "1"
    if prefixRef == "PO":
        fcStep = "P"
        obj = PDSHeader.objects.get(id=id)
        ### Get Supplier Information
        supplier = COOR.objects.filter(FCCODE=obj.forecast_id.supplier_id.code).first()
        # ordH = None
        PREFIX_DTE_Y = str(int(obj.pds_date.strftime('%Y')) + 543)[2:]
        PREFIX_DTE_M = f"{int(obj.pds_date.strftime('%m')):02d}"
        lastNum = OrderH.objects.filter(FCREFTYPE='PO',FCBOOK='H2tsKd02',FDDATE__lte=f"{obj.pds_date.strftime('%Y-%m-')}01").order_by('-FCCODE').first()
        if lastNum is None:
            lastNum = "0000000"
            
        fccodeNo = f"{PREFIX_DTE_Y}{PREFIX_DTE_M}{(int(str(lastNum)[4:]) + 1):04d}"
        
        #### CheckLast No
        lst = CheckLastPurchaseRunning.objects.filter(last_date=f"{PREFIX_DTE_Y}{PREFIX_DTE_M}").count()
        if lst > 0:
            lastNum = CheckLastPurchaseRunning.objects.filter(last_date=f"{PREFIX_DTE_Y}{PREFIX_DTE_M}").order_by('-last_running').first()
            fccodeNo = int(str(lastNum.last_running)) + 1
        
        prNo = f"{str(ordBook.FCPREFIX).strip()}{fccodeNo}"### PO TEST REFNO
        #### Create Last No Log
        lst = CheckLastPurchaseRunning()
        lst.last_date = f"{PREFIX_DTE_Y}{PREFIX_DTE_M}"
        lst.last_running = fccodeNo
        lst.last_no = prNo
        lst.is_active = True
        lst.save()
        
        msg = f"message=เรียนแผนก PU\nขณะนี้ทางแผนก Planning ได้ทำการเปิดเอกสาร{str(ordBook.FCNAME).strip()} เลขที่ {prNo} เรียบร้อยแล้วคะ"
        
        ordH = OrderH()
        ordH.FCSKID=nanoid.generate(size=8)
        ordH.FDDUEDATE=request.POST.get("pds_delivery_date")
        ordH.FCCODE=fccodeNo
        ordH.FCREFNO=prNo
        ordH.FCREFTYPE=prefixRef
        ordH.FCDEPT=dept.FCSKID
        ordH.FCSECT=sect.FCSKID
        ordH.FCBOOK=ordBook.FCSKID
        ordH.FCCREATEBY=emp.FCSKID
        ordH.FCAPPROVEB=""
        ordH.FCCOOR=supplier.FCSKID
        ordH.FCCORP=corp.FCSKID
        ordH.FDDATE=obj.pds_date
        ordH.FNAMT=obj.qty
        ordH.FCSTEP=fcStep
        ordH.save()
        
        obj.ref_formula_id = ordH.FCSKID
        
        ### Create Confirm Invoice
        confirmInv = ConfirmInvoiceHeader()
        confirmInv.approve_by_id = request.user
        confirmInv.pds_id = obj
        confirmInv.supplier_id = obj.supplier_id
        confirmInv.part_model_id = obj.part_model_id
        confirmInv.purchase_no = ordH.FCREFNO
        confirmInv.inv_date = datetime.now()
        confirmInv.inv_delivery_date = obj.pds_delivery_date
        confirmInv.item = 0
        confirmInv.qty = 0
        confirmInv.original_qty = 0
        confirmInv.is_active = True
        confirmInv.save()
        
        ordDetail = PDSDetail.objects.filter(pds_header_id=obj, qty__gt=0).all()
        seq = 1
        qty = 0
        summary_price = 0
        summary_balance = 0
        SUM_FNQTY = 0
        for i in ordDetail:
            #### Sum Balance
            summary_balance += i.balance_qty
            if i.is_select is True and i.qty > 0:
                ordProd = PROD.objects.filter(FCCODE=i.forecast_detail_id.product_id.code,FCTYPE=i.forecast_detail_id.product_id.prod_type_id.code).first()
                unitObj = UM.objects.filter(FCCODE=i.forecast_detail_id.product_id.unit_id.code).first()
                summary_price += int(ordProd.FNSTDCOST) * i.qty
                currentPrice = int(ordProd.FNSTDCOST) * i.qty
                ### Get PR Data
                ordPR = OrderI.objects.get(FCSKID=i.forecast_detail_id.ref_formula_id)
                olderQty = int(ordPR.FNBACKQTY)
                
                # print(f"PR BackQTY: %s" %olderQty)
                ordI = OrderI()
                ordI.FCSKID=nanoid.generate(size=8)
                ordI.FCCOOR=supplier.FCSKID
                ordI.FCCORP=corp.FCSKID
                ordI.FCDEPT=dept.FCSKID
                ordI.FCORDERH=ordH.FCSKID
                ordI.FCPROD=ordProd.FCSKID
                ordI.FCPRODTYPE=ordProd.FCTYPE
                ordI.FCREFTYPE=prefixRef
                ordI.FCSECT=sect.FCSKID
                ordI.FCSEQ=f"{seq:03d}"
                ordI.FCSTUM=unitObj.FCSKID
                ordI.FCUM=unitObj.FCSKID
                ordI.FCUMSTD=unitObj.FCSKID
                ordI.FDDATE=obj.pds_date
                ordI.FNQTY=i.qty
                ordI.FMREMARK=i.remark
                #### Update Nagative to Positive
                ordI.FNBACKQTY=abs(int(i.qty)-olderQty)
                ######
                ordI.FNPRICE=currentPrice
                ordI.FNPRICEKE=currentPrice
                ordI.FCSHOWCOMP=""
                ordI.FCSTEP=fcStep
                ordI.save()
                print(ordI)
                print(f"supplier.FCSKID: {supplier.FCSKID}")
                
                
                ### Update BackQTY For PR
                if ordPR is not None:
                    ordPR.FNBACKQTY=abs(int(i.qty)-olderQty)
                    ordPR.save()
                SUM_FNQTY += ordI.FNQTY
                
                ### Create Notecut
                orderPRID = obj.forecast_id.ref_formula_id
                orderPRDetailID = i.forecast_detail_id.ref_formula_id
                
                ### Update PR to FCSTEP='P'
                prHeader = OrderH.objects.get(FCSKID=orderPRID)
                prHeader.FCSTEP = fcStep
                prHeader.save()
                
                prDetail = OrderI.objects.get(FCSKID=orderPRDetailID)
                prDetail.FCSTEP = fcStep
                prDetail.save()
                #### End Update FCSTEP
                
                ### Create Invoice Details
                invDetail = ConfirmInvoiceDetail()
                invDetail.invoice_header_id = confirmInv
                invDetail.pds_detail_id = i
                invDetail.seq = seq
                invDetail.qty = i.qty
                invDetail.confirm_qty = i.qty
                invDetail.total_qty = i.qty
                invDetail.price = int(ordProd.FNSTDCOST)
                invDetail.remark = ""
                invDetail.ref_formula_id = ordI.FCSKID
                invDetail.save()
                
                ### Save Invoice Detail
                orderPOID = ordH.FCSKID
                orderPODetailID = ordI.FCSKID
                
                ### Create Notecut
                noteCut = NoteCut(
                        FCAPPNAME="",
                        FCSKID=nanoid.generate(size=8),
                        FCCHILDH=orderPRID,
                        FCCHILDI=orderPRDetailID,
                        FCMASTERH=orderPOID,
                        FCMASTERI=orderPODetailID,
                        FNQTY=i.qty,
                        FNUMQTY=i.qty,
                        FCCORRECTB=emp.FCSKID,
                        FCCREATEBY=emp.FCSKID,
                        FCCREATETY="",
                        FCCUACC="",
                        FCDATAIMP="",
                        FCORGCODE="",
                        FCSELTAG="",
                        FCSRCUPD="",
                        FCU1ACC="",
                        FCUDATE="",
                        FCUTIME="",
                        FCCORP=corp.FCSKID
                    )
                noteCut.save()
                # Update Status Order Details
                print(f"QTY: {i.qty} Balance Qty: {i.balance_qty}")
                blQty = i.balance_qty - i.qty
                i.ref_formula_id = ordI.FCSKID
                i.request_status = "1"
                i.qty = blQty
                i.balance_qty = blQty
                i.is_select = i.balance_qty > 0
                i.save()
                
                # Summary Seq/Qty
                seq += 1
                qty += i.qty
        
        ordH.FNAMT=summary_price
        ordH.save()
        # print(f"{ordH.FCREFNO}: {len(ordH.FCREFNO)}")
        # ordDetail = PDSDetail.objects.filter(pds_header_id=obj, qty__gt=0).all()
        # seq = 1
        # qty = 0
        # summary_price = 0
        # summary_balance = 0
        ordDetail = PDSDetail.objects.filter(pds_header_id=obj, qty__gt=0).all()
        seq = 0
        qty = 0
        summary_price = 0
        for i in ordDetail:
            seq += 1
            qty += i.qty
            summary_price += int(i.price) * i.qty
            i.seq = seq
            i.is_select = True
            i.save()
            
        obj.approve_by_id = request.user
        obj.item = seq
        obj.qty = qty
        obj.balance_qty = qty
        obj.summary_price = summary_price
        
        
        if (summary_balance - SUM_FNQTY) == 0:
            obj.pds_status = "2"
            obj.pds_no = ordH.FCREFNO
            obj.ref_formula_id = ordH.FCSKID
            
        else:
            obj.pds_status = "1"
            obj.pds_delivery_date = None
        obj.save()
        
        
        # confirmInv.inv_delivery_date
        # confirmInv.inv_no
        conInvDetail = ConfirmInvoiceDetail.objects.filter(invoice_header_id=confirmInv)
        seq = 0
        qty = 0
        summary_price = 0
        for i in conInvDetail:
            seq += 1
            qty += i.qty
            summary_price += int(i.price) * i.qty
        
        confirmInv.item = seq
        confirmInv.qty = qty
        confirmInv.original_qty = qty
        confirmInv.confirm_qty = qty
        confirmInv.summary_price = summary_price
        confirmInv.inv_status = "0"
        confirmInv.ref_formula_id = ordH.FCSKID
        confirmInv.save()
        
        ### Message Notification
        txtMsg = f"ได้ทำการเปิดเอกสาร PDS เลขที่ {ordH.FCREFNO}"
        msg = f"message=เรียนแผนก PU \nขณะนี้ทางแผนก Planning ได้ทำการเปิดเอกสาร PDS เลขที่ {ordH.FCREFNO} เรียบร้อยแล้วคะ"
        try:
            requests.request("POST", "https://notify-api.line.me/api/notify", headers=headers, data=msg.encode("utf-8"))
        except:
            pass
    else:
        ### Create PR
        obj = Forecast.objects.get(id=id)
        ### Create PDSHeader
        pdsHead = None
        pdsCount = PDSHeader.objects.filter(pds_date=dte).count() + 1
        pds_no = f"PDS{str(dte.strftime('%Y%m'))[3:]}{pdsCount:04d}"
        try:
            pdsHead = PDSHeader.objects.get(forecast_id=obj)
        except PDSHeader.DoesNotExist:
            pdsHead = PDSHeader()
            pass
        
        pdsHead.forecast_id = obj
        pdsHead.supplier_id = obj.supplier_id
        pdsHead.part_model_id = obj.part_model_id
        pdsHead.forecast_plan_id = obj.forecast_plan_id
        pdsHead.pds_date = datetime.now()
        pdsHead.pds_revise_id = obj.forecast_revise_id
        pdsHead.pds_on_month_id = obj.forecast_on_month_id
        pdsHead.pds_on_year_id = obj.forecast_on_year_id
        pdsHead.pds_no = pds_no
        pdsHead.item = 0
        pdsHead.qty = 0
        pdsHead.balance_qty = 0
        pdsHead.summary_price = 0
        pdsHead.pds_status = "0"
        pdsHead.is_active = True
        pdsHead.save()
        ### End PDSHeader
        
        supplier = COOR.objects.filter(FCCODE=obj.supplier_id.code).first()
        ordH = None
        if obj.ref_formula_id is None:
            ### Create PR to Formula
            # #### Create Formula OrderH
            PREFIX_DTE_Y = str(int(obj.forecast_date.strftime('%Y')) + 543)[2:]
            PREFIX_DTE_M = f"{int(obj.forecast_date.strftime('%m')):02d}"
            lastNum = OrderH.objects.filter(FDDATE__lte=obj.forecast_date).order_by('-FCCODE').first()
            if lastNum is None:
                lastNum = "0000000"
                
            fccodeNo = f"{PREFIX_DTE_Y}{PREFIX_DTE_M}{int(str(lastNum)[4:]) + 1:04d}"
            prNo = f"{str(ordBook.FCPREFIX).strip()}{fccodeNo}"### PR TEST REFNO
            msg = f"message=เรียนแผนก Planning\nขณะนี้ทางแผนก PU ได้ทำการอนุมัติเอกสาร {prNo} เรียบร้อยแล้วคะ"
            ordH = OrderH()
            ordH.FCCODE = fccodeNo
            ordH.FCREFNO = prNo
            ordH.FCSKID=nanoid.generate(size=8)
            obj.ref_formula_id = ordH.FCSKID
            
        else:
            ordH = OrderH.objects.get(FCSKID=obj.ref_formula_id)
            msg = f"message=เรียนแผนก Planning\nขณะนี้ทางแผนก PU ได้ทำการอนุมัติเอกสาร {ordH.FCREFNO} เรียบร้อยแล้วคะ"
            pass
        
        ordH.FCREFTYPE=prefixRef
        ordH.FCDEPT=dept.FCSKID
        ordH.FCSECT=sect.FCSKID
        ordH.FCBOOK=ordBook.FCSKID
        ordH.FCCREATEBY=emp.FCSKID
        ordH.FCAPPROVEB=""
        ordH.FCCOOR=supplier.FCSKID
        ordH.FCCORP=corp.FCSKID
        ordH.FDDATE=obj.forecast_date
        ordH.FDDUEDATE=obj.forecast_date
        ordH.FNAMT=0
        ordH.FCSTEP=fcStep
        ordH.save()
        # ### OrderI
        # # Get Order Details
        ordDetail = ForecastDetail.objects.filter(forecast_id=obj, request_qty__gt=0).all()
        seq = 1
        qty = 0
        summary_price = 0
        for i in ordDetail:
            ### Create OrderI Formula
            try:
                ordProd = PROD.objects.filter(FCCODE=i.product_id.code,FCTYPE=i.product_id.prod_type_id.code).first()
                unitObj = UM.objects.filter(FCCODE=i.product_id.unit_id.code).first()
                summary_price += int(ordProd.FNSTDCOST) * int(i.request_qty)
                currentPrice = int(ordProd.FNSTDCOST) * int(i.request_qty)
                ### Create PDS Detail
                pdsDetail = None
                try:
                    pdsDetail = PDSDetail.objects.get(pds_header_id=pdsHead,forecast_detail_id=i)
                except PDSDetail.DoesNotExist:
                    pdsDetail = PDSDetail()
                    pdsDetail.pds_header_id = pdsHead
                    pdsDetail.forecast_detail_id = i
                    pass
                
                pdsDetail.seq = seq
                pdsDetail.qty = i.request_qty
                pdsDetail.balance_qty = i.request_qty
                pdsDetail.price = currentPrice
                # pdsDetail.total_seq = seq
                # pdsDetail.total_qty = i.request_qty
                # pdsDetail.total_balance_qty = i.request_qty
                # pdsDetail.total_price = currentPrice 
                pdsDetail.remark = i.remark
                pdsDetail.is_active = True
                pdsDetail.pds_detail_status = "0"
                pdsDetail.save()
                ### End PDS Detail
            
                ordI = None
                try:
                    ordI = OrderI.objects.get(FCSKID=i.ref_formula_id)
                except OrderI.DoesNotExist as e:
                    ordI = OrderI()
                    ordI.FCSKID=nanoid.generate(size=8)
                    pass
                
                ordI.FCCOOR=supplier.FCSKID
                ordI.FCCORP=corp.FCSKID
                ordI.FCDEPT=dept.FCSKID
                ordI.FCORDERH=ordH.FCSKID
                ordI.FCPROD=ordProd.FCSKID
                ordI.FCPRODTYPE=ordProd.FCTYPE
                ordI.FCREFTYPE=prefixRef
                ordI.FCSECT=sect.FCSKID
                ordI.FCSEQ=f"{seq:03d}"
                ordI.FCSTUM=unitObj.FCSKID
                ordI.FCUM=unitObj.FCSKID
                ordI.FCUMSTD=unitObj.FCSKID
                ordI.FDDATE=obj.forecast_date
                ordI.FNQTY=i.request_qty
                ordI.FMREMARK=i.remark
                ordI.FNBACKQTY=i.request_qty
                ordI.FCSTEP = fcStep
                ######
                ordI.FNPRICE=currentPrice
                ordI.FNPRICEKE=currentPrice
                ordI.FCSHOWCOMP=""
                ordI.save()
                # Update Status Order Details
                i.ref_formula_id = ordI.FCSKID
                i.request_status = "1"
                
            except Exception as e:
                messages.error(request, str(e))
                ordH.delete()
                return
            # Summary Seq/Qty
            seq += 1
            qty += i.request_qty
            i.save()
            
        ordH.FNAMT = summary_price
        ordH.save()
            
        pdsHead.item = (seq - 1)
        pdsHead.qty = qty
        pdsHead.balance_qty = qty
        pdsHead.summary_price = summary_price
        # ### Original
        # pdsHead.total_item = (seq - 1)
        # pdsHead.total_qty = qty
        # pdsHead.total_balance_qty = qty
        # pdsHead.total_summary_price = summary_price
        pdsHead.save()
            
        obj.forecast_no = ordH.FCREFNO
        obj.forecast_status = "1"
        obj.forecast_qty = qty
        obj.forecast_item = (seq - 1)
        obj.save()
        
        ### Message Notification
        txtMsg = f"ได้ทำการอนุมัติเอกสาร {obj.forecast_no}"
        msg = f"message=เรียนแผนก Planning\nขณะนี้ทางแผนก PU ได้ทำการอนุมัติเอกสาร {obj.forecast_no} เรียบร้อยแล้วคะ"
        requests.request("POST", "https://notify-api.line.me/api/notify", headers=headers, data=msg.encode("utf-8"))
        # messages.success(request, f"บันทึกข้อมูลเรียบร้อยแล้ว")
    
    rp = UserErrorLog()
    rp.user_id = request.user
    rp.remark = txtMsg
    rp.is_status = True
    rp.save()
    # except Exception as ex:
    #     messages.error(request, str(ex))
    #     rp = UserErrorLog()
    #     rp.user_id = request.user
    #     rp.remark = f"เกิดข้อผิดพลาด {str(ex)}"
    #     rp.is_status = True
    #     rp.save()
    #     ordH.delete()
    #     return False
    #     # pass
    
    return True

def upload_file_forecast(request, obj, form, change):
    try:
        isAllErrors = 0
        ### Read Excel data
        data = pd.read_excel(request.FILES['file_forecast'], sheet_name=0)
        ### - To Nan
        data.replace('-', np.nan, inplace=True)
        
        ### VCST To Nan
        data.replace('VCST', np.nan, inplace=True)
        
        ### Nan to 0
        data.fillna(0, inplace=True)
        df = data.to_records()
        docs = []
        i = 0
        for r in df:
            if i > 0:
                rows = int(r[0]) + 2
                partNo = str(r[2]).strip()
                partCode = str(r[3]).strip()
                partDescription = str(r[4]).strip()
                supName = str(r[5]).strip()
                partModel = str(r[6]).strip()
                rev0 = int(r[7])
                rev1 = int(r[8])
                rev2 = int(r[9])
                rev3 = int(r[10])
                month0 = 0
                month1 = int(r[11])
                month2 = int(r[12])
                month3 = int(r[13])
                
                isError = False
                msgProduct = ""
                msgSup = ""
                msgPartModel = ""
                description  = ""
                part = None
                if partCode == "0":
                    isError = True
                    msgProduct = f"ไม่ระบุ Part Code"
                    
                else:
                    part = Product.objects.filter(code=str(partCode).strip()).count()
                    if part == 0:
                        msgProduct = f"ไม่พบข้อมูล Part:{partNo}"
                        isError = True
                
                supFilter = None
                if supName == "0":
                    isError = True
                    msgSup = f"ไม่ระบุ Sup."
                    
                else:                   
                    supFilter = Supplier.objects.filter(code=str(supName).strip()).count()
                    if supFilter == 0:
                        isError = True
                        msgSup = f"ไม่พบข้อมูล Sup:{supName}"
                        
                # partModelFilter = None
                # if partModel == "0":
                #     isError = True
                #     msgPartModel = f"ไม่ระบุ Model."
                    
                # else:                   
                #     partModelFilter = ProductGroup.objects.filter(code=str(partModel).strip()).count()
                #     if partModelFilter == 0:
                #         isError = True
                #         msgPartModel = f"ไม่พบข้อมูล Model:{partModel}"
                        
                
                # try:
                #     partFormula = PROD.objects.get(FCCODE=str(partCode).strip())
                #     # print(partFormula)
                # except PROD.DoesNotExist:
                #     print(f"Not Found: {partCode}")
                # print(partModel)
                # print(f"====")
                ### Check revise type
                qty = rev0
                if obj.forecast_revise_id.code == 1:
                    qty = rev1
                    
                elif obj.forecast_revise_id.code == 2:
                    qty = rev2
                    
                elif obj.forecast_revise_id.code == 3:
                    qty = rev3
                
                docs.append({
                    "rows": rows,
                    "partNo": partNo,
                    "partCode": partCode,
                    "partDescription": partDescription,
                    "supName": supName,
                    "partModel": partModel,
                    "rev0": rev0,
                    "rev1": rev1,
                    "rev2": rev2,
                    "rev3": rev3,
                    "qty": qty,
                    "month0": qty,
                    "month1": month1,
                    "month2": month2,
                    "month3": month3,
                })
                if isError:
                    # description = str(f"{msgSup} {msgProduct} {msgPartModel} บรรทัดที่ {rows}").lstrip()
                    description = str(f"{msgSup} {msgProduct} บรรทัดที่ {rows}").lstrip()
                    
                    logError = ForecastErrorLogs()
                    logError.file_name = str(obj.id)
                    logError.row_num=rows
                    logError.item=i
                    logError.part_code=partCode
                    logError.part_no=partNo
                    logError.part_name=partDescription
                    logError.supplier=supName
                    logError.model=partModel
                    logError.rev_0=rev0
                    logError.rev_1=rev1
                    logError.rev_2=rev2
                    logError.rev_3=rev3
                    logError.remark=description
                    logError.is_error=isError
                    logError.is_success=False
                    logError.save()
                    isAllErrors += 1
                
            i += 1
        
        if isAllErrors > 0:
            messages.warning(request, format_html("{} <a class='text-primary' href='/forecast/logging/{}'>{}</a>", f"เกิดข้อผิดพลาดไม่สามารถอัพโหลดข้อมูลได้", str(obj.id), "รบกวนกดที่ลิงค์นี้เพื่อตรวจข้อผิดพลาดดังกล่าว"))
            obj.delete()
            return
            
        else:
            # ### Create File Forecast Upload
            # mydate = datetime.now()
            # onMonth = int(mydate.month)
            # onYear = int(mydate.year)
            
            # if obj.forecast_month is None:
            #     onMonthList = OnMonthList.objects.get(value=str(onMonth))
            #     obj.forecast_month = onMonthList
                
            # else:
            #     if obj.forecast_month.value != onMonth:
            #         messages.warning(request, "กรุณาเลือกเดือน Forecast ให้ถูกต้องด้วย")
            #         return
                    

            # if obj.forecast_year is None:
            #     onYearList = OnYearList.objects.get(value=str(onYear))
            #     obj.forecast_year = onYearList
                
            # else:
            #     if obj.forecast_year.value != onYear:
            #         messages.warning(request, "กรุณาเลือกปี Forecast ให้ถูกต้องด้วย")
            #         return
            
            if obj.forecast_book_id is None:
                bookData = Book.objects.get(id=request.POST.get('forecast_book_id'))
                if len(request.POST.get('forecast_book_id')) == 0: 
                    reviseData = ReviseBook.objects.get(name='Upload EDI') 
                    bookData = Book.objects.get(id=reviseData.book_id)
                    obj.forecast_book_id = bookData
            ### Save Data
            obj.is_generated = True
            obj.save()
            
            planForecast = PlanningForecast.objects.get(plan_month=str(obj.forecast_month.value), plan_year=obj.forecast_year.value)
            sectionData = request.user.section_id
            if request.user.section_id is None:
                sectionData = Section.objects.get(code="-")
                
            for r in docs:
                part = Product.objects.get(code=str(r['partCode']).strip())
                supFilter = Supplier.objects.get(code=str(r['supName']).strip())
                # partModel = ProductGroup.objects.get(code=str(r['partModel']).strip())
                pdsHeader = None
                try:
                    pdsHeader = Forecast.objects.get(file_forecast_id=obj,supplier_id=supFilter,forecast_plan_id=planForecast,forecast_revise_id=obj.forecast_revise_id, part_model_id=part.prod_group_id)
                    
                except Forecast.DoesNotExist as ex:
                    rndNo = f"FC{str(obj.forecast_date.strftime('%Y%m'))[3:]}"
                    rnd = f"{rndNo}{(Forecast.objects.filter(forecast_no__gte=rndNo).count() + 1):05d}"
                    pdsHeader = Forecast()
                    pdsHeader.forecast_plan_id=planForecast
                    pdsHeader.file_forecast_id=obj
                    pdsHeader.supplier_id=supFilter
                    pdsHeader.part_model_id=part.prod_group_id
                    pass
                
                pdsHeader.section_id=sectionData
                pdsHeader.book_id=obj.forecast_book_id
                pdsHeader.forecast_no=rnd
                pdsHeader.forecast_date=obj.forecast_date
                pdsHeader.forecast_revise_id=obj.forecast_revise_id
                pdsHeader.forecast_on_month_id=obj.forecast_month
                pdsHeader.forecast_on_year_id=obj.forecast_year
                pdsHeader.forecast_by_id=request.user
                pdsHeader.forecast_status="0"
                pdsHeader.save()
                ### Create PDS Detail
                pdsDetail = None
                try:
                    pdsDetail = ForecastDetail.objects.get(forecast_id=pdsHeader,product_id=part)
                    
                except ForecastDetail.DoesNotExist as ex:
                    pdsDetail = ForecastDetail()
                    pdsDetail.forecast_id=pdsHeader
                    pdsDetail.product_id=part
                    pass
                
                pdsDetail.request_qty=r["qty"]
                pdsDetail.balance_qty=r["qty"]
                pdsDetail.month_0 = str(r['month0'])
                pdsDetail.month_1 = str(r['month1'])
                pdsDetail.month_2 = str(r['month2'])
                pdsDetail.month_3 = str(r['month3'])
                pdsDetail.price=part.price
                pdsDetail.request_by_id=request.user
                pdsDetail.request_status="0"
                pdsDetail.import_model_by_user=r['partModel']
                pdsDetail.save()
                
            #####
            forecastData = Forecast.objects.filter(file_forecast_id=obj.id)
            for pHeader in forecastData:
                items = ForecastDetail.objects.filter(forecast_id=pHeader)
                rNum = 0
                rQty = 0
                rPrice = 0
                rMonth0 = 0
                rMonth1 = 0
                rMonth2 = 0
                rMonth3 = 0
                for r in items:
                    rQty += r.request_qty
                    rPrice += int(r.product_id.price)
                    rMonth0 += r.month_0
                    rMonth1 += r.month_1
                    rMonth2 += r.month_2
                    rMonth3 += r.month_3
                    rNum += 1
                    r.seq = rNum
                    r.save()
                    
                pHeader.forecast_item = rNum
                pHeader.forecast_qty = rQty
                pHeader.forecast_total_qty = rQty
                pHeader.forecast_price = rPrice
                pdsHeader.forecast_m0 = rMonth0
                pdsHeader.forecast_m1 = rMonth1
                pdsHeader.forecast_m2 = rMonth2
                pdsHeader.forecast_m3 = rMonth3                
                pHeader.save()
                
            messages.success(request, f"Upload {str(obj.id)} Successfully")
            #### Send notification
            token = os.environ.get("LINE_TOKEN")
            if type(request.user.line_notification_id) != type(None):
                token = request.user.line_notification_id.token
            
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': f'Bearer {token}'
            }
            
            msg = f"message=เรียนแผนก PU\nขณะนี้ทางแผนก Planning\nทำการอัพโหลด Forecast({pHeader.forecast_plan_id}) {pHeader.forecast_revise_id.name}\nกรุณาทำการยืนยันให้ด้วยคะ"
            try:
                requests.request("POST", "https://notify-api.line.me/api/notify", headers=headers, data=msg.encode("utf-8"))
            except:
                pass
            
            #### Create Logging
            rp = UserErrorLog()
            rp.user_id = request.user
            rp.remark = f"Upload Forecast {obj.file_forecast}"
            rp.is_status = True
            rp.save()
        
    except Exception as ex:
        messages.error(request, f"รูปแบบเอกสารที่ใช้อัพโหลดข้อมูลไม่ถูกต้อง {str(ex)}")
        #### Create Logging
        rp = UserErrorLog()
        rp.user_id = request.user
        rp.remark = f"รูปแบบเอกสารที่ใช้อัพโหลดข้อมูลไม่ถูกต้อง {str(ex)}"
        rp.is_status = False
        rp.save()
        obj.delete()
        return
    
    return obj

def request_validation(request):
    Forecast._meta.verbose_name_plural = "Upload Forecast"
    PDSHeader._meta.verbose_name_plural = "Open PDS"
    ConfirmInvoiceHeader._meta.verbose_name_plural = "View Purchase"
    confirm_invoice_apps.ConfirmInvoicesConfig.verbose_name = "คำสั่งซื้อสินค้า"
    ReceiveHeader._meta.verbose_name_plural = "View Receive"
    receive_apps.ReceivesConfig.verbose_name = "จัดการข้อมูล Receive"
    
    
    query_set = Group.objects.filter(user=request.user)
    if query_set.filter(name="Planning").exists():
        Forecast._meta.verbose_name_plural = "Upload Forecast"
        PDSHeader._meta.verbose_name_plural = "Open PDS"
        forecast_apps.ForecastsConfig.verbose_name = "อัพโหลด Forecast"
        open_pds_apps.OpenPdsConfig.verbose_name = "จัดการข้อมูล PDS"
        
    if query_set.filter(name="Purchase").exists():
        Forecast._meta.verbose_name_plural = "Open PR"
        PDSHeader._meta.verbose_name_plural = "View PDS"
        forecast_apps.ForecastsConfig.verbose_name = "จัดการข้อมูล Purchase"
        open_pds_apps.OpenPdsConfig.verbose_name = "ตรวจสอบ PDS"
    
    if query_set.filter(name="Supplier").exists():
        Forecast._meta.verbose_name_plural = "View Forecast"
        PDSHeader._meta.verbose_name_plural = "View PDS"
        ConfirmInvoiceHeader._meta.verbose_name_plural = "Confirm Invoice"
        forecast_apps.ForecastsConfig.verbose_name = "ตรวจสอบ Forecast"
        open_pds_apps.OpenPdsConfig.verbose_name = "ตรวจสอบ PDS"
        confirm_invoice_apps.ConfirmInvoicesConfig.verbose_name = "ยืนยันการส่งสินค้า"
        ReceiveHeader._meta.verbose_name_plural = "View Delivery"
        receive_apps.ReceivesConfig.verbose_name = "จัดการข้อมูล Delivery"
    pass

def check_confirm_qty(request):
    data = request.POST.copy()
    # confirmID = data['confirminvoicedetail_set-0-invoice_header_id']
    totalConfirm = 0
    plimit = int(data['confirminvoicedetail_set-TOTAL_FORMS'])
    for i in range(0, plimit):
        id = data[f'confirminvoicedetail_set-{i}-id']
        confirmQty = int(data[f'confirminvoicedetail_set-{i}-confirm_qty'])
        obj = ConfirmInvoiceDetail.objects.get(id=id)
        # print(f"Confirm QTY: {confirmQty} QTY: {obj.qty} :: {int(obj.qty)-confirmQty}")
        if confirmQty > int(obj.qty):
            obj.confirm_qty = obj.qty
            # obj.save()
            return True
        
        obj.balance_qty = int(obj.qty)
        balance_qty = int(obj.qty)-confirmQty
        obj.qty=balance_qty
        obj.confirm_status = "1"
        obj.save()
        totalConfirm += int(obj.qty)-confirmQty
    
    # print(confirmID)
    # conData = ConfirmInvoiceHeader.objects.get(id=confirmID)
    # print(conData)
    # conData.qty = totalConfirm
    # conData.confirm_qty = totalConfirm
    # conData.save()
    return False

def receive_invoice(request, obj):
    dte = datetime.now()
    rnd = ReceiveHeader.objects.filter(confirm_invoice_id=obj).count()
    recNo = f"REC{str(dte.strftime('%Y%m%d'))[3:]}{(rnd+1):05d}"
    rec = ReceiveHeader()
    rec.receive_by_id = request.user
    rec.confirm_invoice_id = obj
    rec.supplier_id = obj.supplier_id
    rec.part_model_id = obj.part_model_id
    rec.purchase_no = obj.purchase_no
    rec.receive_no = recNo
    rec.receive_date = None
    rec.inv_delivery_date = obj.inv_delivery_date
    rec.inv_no = str(obj.inv_no).upper()
    rec.item = 0
    rec.qty = 0
    rec.summary_price = 0
    rec.save()
    
    seq = 0
    qty = 0
    data = request.POST.copy()
    plimit = int(data['confirminvoicedetail_set-TOTAL_FORMS'])
    for i in range(0, plimit):
        id = data[f'confirminvoicedetail_set-{i}-id']
        confirmQty = int(data[f'confirminvoicedetail_set-{i}-confirm_qty'])
        confirmDetail = ConfirmInvoiceDetail.objects.get(id=id)
        totalQty = confirmDetail.balance_qty
        receDetail = ReceiveDetail()
        receDetail.receive_header_id = rec
        receDetail.confirm_detail_id = confirmDetail
        receDetail.seq = seq + 1
        receDetail.qty = confirmQty
        receDetail.save()
        
        ### Update Transaction
        confirmDetail.qty = (totalQty - confirmQty)
        confirmDetail.confirm_qty = (totalQty - confirmQty)
        confirmDetail.balance_qty = 0
        confirmDetail.confirm_status = "1"
        if (totalQty - confirmQty) > 0:
            confirmDetail.confirm_status = "2"
            
        confirmDetail.save()
        seq += 1
        qty += confirmQty
        
    rec.item = seq
    rec.qty = qty
    rec.save()
    
    
    recQty = 0
    objDetail = ConfirmInvoiceDetail.objects.filter(invoice_header_id=obj)
    for i in objDetail:
        rc = ReceiveDetail.objects.filter(confirm_detail_id=i)
        for r in rc:
            # print(r.qty)
            recQty += int(r.qty)
    
    obj.confirm_qty = recQty
    obj.qty = obj.original_qty
    
    if confirmDetail.qty == 0:
        obj.confirm_qty = obj.original_qty
        obj.inv_status = 1
        
    else:
        obj.inv_status = 2
    