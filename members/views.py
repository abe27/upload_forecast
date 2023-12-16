from django.shortcuts import redirect, render
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request, 'index.html')

def sync_master(request):
    messages.success(request, f"บันทึกข้อมูลเรียบร้อยแล้ว")
    return redirect(f"/web/")
