
from rest_framework import serializers
from .models import (Company, Project, Departments, Suppliers, Items, 
    VoucherRequestGet, VoucherSupplier, Voucher, VoucherLine, VoucherItem)

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['company_code']

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['project_code']

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departments
        fields = ['department_code']

class SuppliersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suppliers
        fields = ['supplier_code']
        
class ItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Items
        fields = ['account_code']
        
class VoucherRequestGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoucherRequestGet
        fields = ['voucher_request_no']
        
class VoucherItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoucherItem
        fields = ['quantity', 'unit', 'description', 'amount']

class VoucherLineSerializer(serializers.ModelSerializer):
    items = VoucherItemSerializer(many=True)

    class Meta:
        model = VoucherLine
        fields = ['account_code', 'amount', 'items']

class VoucherSupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoucherSupplier
        fields = ['code', 'name', 'tin']

class VoucherSerializer(serializers.ModelSerializer):
    supplier = VoucherSupplierSerializer()
    lines = VoucherLineSerializer(many=True)

    class Meta:
        model = Voucher
        fields = [
            'voucher_request_no',
            'branch_code',
            'company_code',
            'date_prepared',
            'time_prepared',
            'supplier',
            'total_amount',
            'project_code',
            'lines',
            'prs_username'
        ]

    def create(self, validated_data):
        supplier_data = validated_data.pop('supplier')
        lines_data = validated_data.pop('lines')

        supplier, _ = VoucherSupplier.objects.get_or_create(**supplier_data)
        voucher = Voucher.objects.create(supplier=supplier, **validated_data)

        for line_data in lines_data:
            items_data = line_data.pop('items')
            line = VoucherLine.objects.create(voucher=voucher, **line_data)
            for item_data in items_data:
                VoucherItem.objects.create(line=line, **item_data)

        return voucher
    