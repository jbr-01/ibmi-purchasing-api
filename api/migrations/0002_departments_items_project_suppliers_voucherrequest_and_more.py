# Generated by Django 4.2.3 on 2024-12-16 09:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Departments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department_code', models.IntegerField(default=0)),
                ('department_name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Items',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_code', models.CharField(max_length=8)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_code', models.CharField(max_length=3)),
                ('company_initials', models.CharField(max_length=5)),
                ('company_tin', models.CharField(max_length=18)),
                ('company_contact_no', models.CharField(max_length=8)),
                ('company_address', models.CharField(max_length=90)),
            ],
        ),
        migrations.CreateModel(
            name='Suppliers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('supplier_code', models.CharField(max_length=4)),
            ],
        ),
        migrations.CreateModel(
            name='VoucherRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('voucher_request_no', models.CharField(max_length=12, unique=True)),
                ('reference_no', models.CharField(max_length=20)),
                ('particulars_total_amount', models.DecimalField(decimal_places=2, max_digits=15)),
            ],
        ),
        migrations.CreateModel(
            name='VoucherRequestParticular',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('item_description', models.CharField(max_length=50)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=15)),
                ('voucher_request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='particulars', to='api.voucherrequest')),
            ],
        ),
        migrations.CreateModel(
            name='VoucherRequestHeader',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_code', models.PositiveIntegerField()),
                ('branch', models.PositiveIntegerField()),
                ('project_code', models.CharField(max_length=3)),
                ('date_prepared', models.DateField()),
                ('supplier_code', models.CharField(max_length=4)),
                ('supplier_name', models.CharField(max_length=35)),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=15)),
                ('voucher_type', models.CharField(max_length=1)),
                ('voucher_request', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='header', to='api.voucherrequest')),
            ],
        ),
        migrations.CreateModel(
            name='VoucherRequestDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_code', models.CharField(max_length=50)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=15)),
                ('voucher_request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='details', to='api.voucherrequest')),
            ],
        ),
    ]