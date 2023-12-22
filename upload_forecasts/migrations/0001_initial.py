# Generated by Django 4.2.8 on 2023-12-22 01:48

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ForecastErrorLogs',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='PRIMARY KEY')),
                ('file_name', models.UUIDField(verbose_name='File Forecast')),
                ('row_num', models.IntegerField(verbose_name='Row')),
                ('item', models.IntegerField(verbose_name='Item')),
                ('part_code', models.CharField(max_length=50, verbose_name='Part Code')),
                ('part_no', models.CharField(max_length=50, verbose_name='Part No.')),
                ('part_name', models.CharField(max_length=50, verbose_name='Part Name')),
                ('supplier', models.CharField(max_length=50, verbose_name='Supplier')),
                ('model', models.CharField(max_length=50, verbose_name='Model')),
                ('rev_0', models.IntegerField(blank=True, default=0, null=True, verbose_name='Rev.0')),
                ('rev_1', models.IntegerField(blank=True, default=0, null=True, verbose_name='Rev.1')),
                ('rev_2', models.IntegerField(blank=True, default=0, null=True, verbose_name='Rev.2')),
                ('rev_3', models.IntegerField(blank=True, default=0, null=True, verbose_name='Rev.3')),
                ('rev_4', models.IntegerField(blank=True, default=0, null=True, verbose_name='Rev.4')),
                ('rev_5', models.IntegerField(blank=True, default=0, null=True, verbose_name='Rev.5')),
                ('rev_6', models.IntegerField(blank=True, default=0, null=True, verbose_name='Rev.6')),
                ('rev_7', models.IntegerField(blank=True, default=0, null=True, verbose_name='Rev.7')),
                ('remark', models.TextField(blank=True, null=True, verbose_name='Remark')),
                ('is_error', models.BooleanField(blank=True, default=True, null=True, verbose_name='Is Error')),
                ('is_success', models.BooleanField(blank=True, default=False, null=True, verbose_name='Is Success')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'PDS Error Logging',
                'verbose_name_plural': 'PDS Error Logging',
                'db_table': 'ediForecastErrorLogs',
                'ordering': ('row_num', 'item', 'created_at', 'updated_at'),
            },
        ),
        migrations.CreateModel(
            name='OnMonthList',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='PRIMARY KEY')),
                ('name', models.CharField(max_length=250, unique=True, verbose_name='Name')),
                ('value', models.IntegerField(unique=True, verbose_name='Value')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is Active')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'tbmOnMonthList',
                'ordering': ('value', 'name'),
            },
        ),
        migrations.CreateModel(
            name='OnYearList',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='PRIMARY KEY')),
                ('name', models.CharField(max_length=4, unique=True, verbose_name='Name')),
                ('value', models.IntegerField(unique=True, verbose_name='Value')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is Active')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'tbmOnYearList',
                'ordering': ('value', 'name'),
            },
        ),
        migrations.CreateModel(
            name='UploadForecast',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='PRIMARY KEY')),
                ('file_forecast', models.FileField(upload_to='static/forecasts', verbose_name='File Forecast')),
                ('forecast_date', models.DateField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='Date')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('is_generated', models.BooleanField(blank=True, default=False, null=True, verbose_name='Is Generated')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is Active')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('forecast_book_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.book', verbose_name='Book ID')),
                ('forecast_month', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='upload_forecasts.onmonthlist', verbose_name='Month')),
                ('forecast_revise_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.edirevisetype', verbose_name='Revise')),
                ('forecast_year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='upload_forecasts.onyearlist', verbose_name='Year')),
            ],
            options={
                'db_table': 'tbmUploadForecast',
            },
        ),
    ]
