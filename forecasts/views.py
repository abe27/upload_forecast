from django.shortcuts import redirect, render
from django.contrib import messages

from forecasts import greeter

# Create your views here.
def index(request):
    return redirect("/web/")

def approve_forecast(request, id):
    if greeter.create_purchase_order(request, id):
        messages.success(request, f"บันทึกข้อมูลเรียบร้อยแล้ว")
            
    return redirect(f"/web/forecasts/forecast/{id}/change/")