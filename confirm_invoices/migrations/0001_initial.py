# Generated by Django 4.2.8 on 2023-12-15 08:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('members', '0005_alter_usererrorlog_options_and_more'),
        ('products', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('open_pds', '0002_alter_pdsheader_pds_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='PrintTAG',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parm_id', models.IntegerField(verbose_name='Print TAG ID')),
                ('seq', models.IntegerField(verbose_name='Seq')),
                ('purchase_id', models.UUIDField(verbose_name='Purchase ID')),
                ('purchase_no', models.CharField(max_length=50, verbose_name='PO No.')),
                ('part_no', models.CharField(max_length=255, verbose_name='Part No.')),
                ('part_name', models.CharField(max_length=255, verbose_name='Part Name')),
                ('part_model', models.CharField(max_length=255, verbose_name='Part Model')),
                ('qty', models.IntegerField(verbose_name='Qty')),
                ('unit', models.CharField(max_length=25, verbose_name='Unit')),
                ('lot_no', models.CharField(blank=True, max_length=50, null=True, verbose_name='LotNo.')),
                ('customer_name', models.CharField(max_length=50, verbose_name='Customer')),
                ('print_date', models.CharField(max_length=10, verbose_name='Print Date')),
                ('qr_code', models.CharField(blank=True, max_length=255, null=True, verbose_name='QR Code')),
                ('is_active', models.BooleanField(blank=True, default=False, null=True, verbose_name='Is Active')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'tmpPrintTag',
                'verbose_name_plural': 'tmpPrintTag',
                'db_table': 'tmpPrintTag',
                'ordering': ('seq', 'created_at', 'updated_at'),
            },
        ),
        migrations.CreateModel(
            name='ReportPurchaseOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('SUP_CODE', models.CharField(max_length=255)),
                ('SEQ', models.IntegerField()),
                ('FCCODE', models.CharField(max_length=255)),
                ('FCNAME', models.CharField(max_length=255)),
                ('FDDATE', models.CharField(blank=True, max_length=255, null=True)),
                ('FDDUEDATE', models.CharField(blank=True, max_length=255, null=True)),
                ('FCREFNO', models.CharField(max_length=255)),
                ('FCPARTCODE', models.CharField(max_length=255)),
                ('FCPARTSNAME', models.CharField(max_length=255)),
                ('FCPARTNAME', models.CharField(max_length=255)),
                ('FNQTY', models.FloatField(blank=True, null=True)),
                ('TOTALPRICE', models.FloatField(blank=True, null=True)),
                ('FNBACKQTY', models.FloatField(blank=True, null=True)),
                ('TOTALPRICE_BACKQTY', models.FloatField(blank=True, null=True)),
                ('I_ORDER_DATE', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'verbose_name': 'tmpReportPurchaseOrder',
                'verbose_name_plural': 'tmpReportPurchaseOrder',
                'db_table': 'tmpReportPurchaseOrder',
                'ordering': ('FCCODE', 'SEQ', 'FCREFNO'),
            },
        ),
        migrations.CreateModel(
            name='ConfirmInvoiceHeader',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='PRIMARY KEY')),
                ('purchase_no', models.CharField(blank=True, max_length=15, null=True, verbose_name='PO No.')),
                ('inv_date', models.DateField(blank=True, null=True, verbose_name='Invoice Date')),
                ('inv_delivery_date', models.DateField(blank=True, null=True, verbose_name='Delivery Date')),
                ('inv_no', models.CharField(blank=True, max_length=15, null=True, verbose_name='Invoice No.')),
                ('item', models.IntegerField(verbose_name='Item')),
                ('qty', models.IntegerField(verbose_name='Qty')),
                ('confirm_qty', models.IntegerField(blank=True, default='0', null=True, verbose_name='Confirm Qty')),
                ('summary_price', models.FloatField(blank=True, default='0', null=True, verbose_name='Summary Price')),
                ('remark', models.TextField(blank=True, null=True, verbose_name='Remark')),
                ('inv_status', models.CharField(blank=True, choices=[('0', 'รอยืนยัน'), ('1', 'ยืนยันแล้ว'), ('2', 'จัดส่งไม่ครบ'), ('3', 'ยกเลิก')], default='0', max_length=1, null=True, verbose_name='inv Status')),
                ('ref_formula_id', models.CharField(blank=True, max_length=8, null=True, verbose_name='Formula ID')),
                ('is_download_count', models.IntegerField(blank=True, default='0', null=True, verbose_name='Download Count')),
                ('is_active', models.BooleanField(blank=True, default=False, null=True, verbose_name='Is Active')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('approve_by_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Approve By ID')),
                ('part_model_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.productgroup', verbose_name='Model ID')),
                ('pds_id', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='open_pds.pdsheader', verbose_name='PR No.')),
                ('supplier_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='members.supplier', verbose_name='Supplier ID')),
            ],
            options={
                'verbose_name': 'Confirm Invoice',
                'verbose_name_plural': 'EDI Confirm Invoice',
                'db_table': 'ediConfirmInvoice',
                'ordering': ('inv_status', 'inv_no', 'created_at', 'updated_at'),
                'permissions': [('is_download_report', 'ดูรายงาน'), ('edit_qty', 'แก้ไขจำนวน'), ('print_tag', 'Print TAG')],
            },
        ),
        migrations.CreateModel(
            name='ConfirmInvoiceDetail',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='PRIMARY KEY')),
                ('seq', models.IntegerField(verbose_name='Seq.')),
                ('qty', models.IntegerField(verbose_name='Qty')),
                ('confirm_qty', models.IntegerField(blank=True, default='0', null=True, verbose_name='Confirm Qty')),
                ('total_qty', models.IntegerField(blank=True, default='0', null=True, verbose_name='Total Qty')),
                ('balance_qty', models.IntegerField(blank=True, default='0', null=True, verbose_name='Total Qty')),
                ('price', models.FloatField(blank=True, default='0', null=True, verbose_name='Price')),
                ('remark', models.TextField(blank=True, null=True, verbose_name='Remark')),
                ('ref_formula_id', models.CharField(blank=True, max_length=8, null=True, verbose_name='Formula ID')),
                ('is_select', models.BooleanField(blank=True, default=True, null=True, verbose_name='Is Select')),
                ('is_active', models.BooleanField(blank=True, default=False, null=True, verbose_name='Is Active')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('invoice_header_id', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='confirm_invoices.confirminvoiceheader', verbose_name='PDS ID')),
                ('pds_detail_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='open_pds.pdsdetail', verbose_name='PDS Detail')),
            ],
            options={
                'verbose_name': 'Confirm Invoice Detail',
                'verbose_name_plural': 'Confirm Invoice Detail',
                'db_table': 'ediConfirmInvoiceDetail',
                'ordering': ('seq', 'pds_detail_id', 'created_at', 'updated_at'),
            },
        ),
    ]
