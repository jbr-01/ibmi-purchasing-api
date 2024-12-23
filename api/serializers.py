from datetime import datetime
from rest_framework import serializers
from .models import (Company, VoucherRequest, VoucherRequestHeader,
    VoucherRequestDetail, VoucherRequestParticular)

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['company_code']
    
    def validate_company_code(self, value):
        print('value => ', value)
        if (value > 99):
            raise serializers.ValidationError("Company code must be an integer between 1 and 99.")
        return value

# class CompanySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Company
#         fields = ['company_code']
        
#     # Custom validation for the company_code
#     def validate_company_code(self, value):
#         if value <= 0:
#             raise serializers.ValidationError("Company code must be a positive integer.")
#         return value
        # fields = '__all__'
        # read_only_fields = '__all__'  # Set read-only fields
        
class VoucherRequestHeaderSerializer(serializers.ModelSerializer):
    date_prepared = serializers.CharField()  # Override the field to handle yyyymmdd format

    class Meta:
        model = VoucherRequestHeader
        exclude = ['voucher_request']  # Exclude voucher_request; it will be set automatically
        # fields = '__all__'

    def validate_date_prepared(self, value):
        # Validate and convert yyyymmdd to date
        try:
            return datetime.strptime(value, "%Y%m%d").date()
        except ValueError:
            raise serializers.ValidationError("Date must be in yyyymmdd format.")

    def to_representation(self, instance):
        # Convert date to yyyymmdd when serializing
        representation = super().to_representation(instance)
        if instance.date_prepared:
            representation['date_prepared'] = instance.date_prepared.strftime("%Y%m%d")
        return representation

class VoucherRequestDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoucherRequestDetail
        exclude = ['voucher_request']
        # fields = '__all__'


class VoucherRequestParticularSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoucherRequestParticular
        exclude = ['voucher_request']
        # fields = '__all__'
        
class VoucherRequestSerializer(serializers.ModelSerializer):

    header = VoucherRequestHeaderSerializer()
    detail = VoucherRequestDetailSerializer(many=True)
    particulars = VoucherRequestParticularSerializer(many=True)
    
    class Meta:
        model = VoucherRequest
        fields = ['voucher_request_no', 'reference_no', 'header', 'detail', 'particulars', 'particulars_total_amount']

    def create(self, validated_data):
        header_data = validated_data.pop('header')
        detail_data = validated_data.pop('detail')
        particulars_data = validated_data.pop('particulars')

        # Create the parent VoucherRequest object
        voucher_request = VoucherRequest.objects.create(**validated_data)

        # Create related Header
        VoucherRequestHeader.objects.create(voucher_request=voucher_request, **header_data)
        
        # Create related Details
        for detail in detail_data:
            VoucherRequestDetail.objects.create(voucher_request=voucher_request, **detail)

        # Create related Particulars
        for particular in particulars_data:
            VoucherRequestParticular.objects.create(voucher_request=voucher_request, **particular)

        return voucher_request