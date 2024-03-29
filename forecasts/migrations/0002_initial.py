# Generated by Django 4.2.8 on 2023-12-22 01:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0001_initial'),
        ('upload_forecasts', '0001_initial'),
        ('members', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('forecasts', '0001_initial'),
        ('books', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='forecastdetail',
            name='request_by_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Request By ID'),
        ),
        migrations.AddField(
            model_name='forecast',
            name='book_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='books.book', verbose_name='Book ID'),
        ),
        migrations.AddField(
            model_name='forecast',
            name='file_forecast_id',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='upload_forecasts.uploadforecast', verbose_name='Forecast ID'),
        ),
        migrations.AddField(
            model_name='forecast',
            name='forecast_by_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Request By ID'),
        ),
        migrations.AddField(
            model_name='forecast',
            name='forecast_on_month_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='upload_forecasts.onmonthlist', verbose_name='Request On Month'),
        ),
        migrations.AddField(
            model_name='forecast',
            name='forecast_on_year_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='upload_forecasts.onyearlist', verbose_name='Request On Year'),
        ),
        migrations.AddField(
            model_name='forecast',
            name='forecast_plan_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='members.planningforecast', verbose_name='Forecast Plan'),
        ),
        migrations.AddField(
            model_name='forecast',
            name='forecast_revise_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='books.edirevisetype', verbose_name='Revise ID'),
        ),
        migrations.AddField(
            model_name='forecast',
            name='part_model_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.productgroup', verbose_name='Model ID'),
        ),
        migrations.AddField(
            model_name='forecast',
            name='section_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='members.section', verbose_name='Section ID'),
        ),
        migrations.AddField(
            model_name='forecast',
            name='supplier_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='members.supplier', verbose_name='Supplier ID'),
        ),
    ]
