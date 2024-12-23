from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .db_utils import (companies, projects, departments, suppliers, items, payment_processing)
from .serializers import CompanySerializer, VoucherRequestSerializer

class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "This is a protected view!"})
    
class CompanyListView(APIView):
    def get(self, request):
        companiesList = companies.fetch_all_companies()
        return Response(companiesList)
    
class CompanyDetailView(APIView):
    def get(self, request, company_code):
        print('request => ', request)
        serializer = CompanySerializer(data=request.data)
        print('isvalid', serializer.is_valid())
        if serializer.is_valid():
            company = companies.fetch_company_by_id(company_code)
            if company:
                return Response(company)
            return Response({"error": "Company not found"}, status=404)

        
    # def get(self, request, company_code, *args, **kwargs):
    #     # Validate path parameters using the serializer
    #     serializer = CompanySerializer(data=kwargs)
    #     serializer.is_valid(raise_exception=True)  # Raise error if validation fails
        
    #     validated_data = serializer.validated_data
    #     return Response({"message": "Validated successfully", "data": validated_data})

        # Retrieve the company based on the path parameter
        # company = companies.fetch_company_by_id(company_code)
        # if company:
        #     return Response(company)
        # return Response({"error": "Company not found"}, status=404)

        # Serialize the company data
        # serializer = CompanySerializer(company)
        # return Response(serializer.data)
        
        # serializer = CompanySerializer(company_code)
        # return Response(serializer.data)
        # company = companies.fetch_company_by_id(company_code)
        # if company:
        #     return Response(company)
        # return Response({"error": "Company not found"}, status=404)

class ProjectListView(APIView):
    def get(self, request):
        projectsList = projects.fetch_all_projects()
        return Response(projectsList)

class ProjectDetailView(APIView):
    def get(self, request, project_code):
        project = projects.fetch_project_by_id(project_code)
        if project:
            return Response(project)
        return Response({"error": "Project not found"}, status=404)
    
class DepartmentListView(APIView):
    def get(self, request):
        departmentsList = departments.fetch_all_departments()
        return Response(departmentsList)

class DepartmentDetailView(APIView):
    def get(self, request, department_code):
        department = departments.fetch_department_by_id(department_code)
        if department:
            return Response(department)
        return Response({"error": "Department not found"}, status=404)

class SupplierListView(APIView):
    def get(self, request):
        suppliersList = suppliers.fetch_all_suppliers()
        return Response(suppliersList)

class SupplierDetailView(APIView):
    def get(self, request, supplier_code):
        supplier = suppliers.fetch_supplier_by_id(supplier_code)
        if supplier:
            return Response(supplier)
        return Response({"error": "Supplier not found"}, status=404)

class ItemListView(APIView):
    def get(self, request):
        itemsList = items.fetch_all_items()
        return Response(itemsList)

class ItemDetailView(APIView):
    def get(self, request, item_code):
        item = items.fetch_item_by_id(item_code)
        if item:
            return Response(item)
        return Response({"error": "Item not found"}, status=404)
    
class VoucherRequestListView(APIView):
    def post(self, request):
        serializer = VoucherRequestSerializer(data=request.data)
        
        if serializer.is_valid():
            res = payment_processing.add_voucher_request(request.data)
            
            if res["status"] == 'success':
                return Response(res, status=200)
            return Response(res, status=409 if res["data"]["voucher_request_no"] else 400)
            # return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
        # res = payment_processing.add_voucher_request(data)
        
        # if res["status"] == 'success':
        #     return Response(res, status=200)
        # return Response(res, status=409 if res["data"]["voucher_request_no"] else 400)
    
class VoucherRequestDetailView(APIView):
    def get(self, request, voucher_request_no):
        voucher_request = payment_processing.fetch_voucher_request_by_id(voucher_request_no)
        if "data" in voucher_request:
            return Response(voucher_request['data'])
        else:
            if "error" in voucher_request.values():
                return Response(voucher_request, status=404)
            return Response({"error": "Voucher Request not found"}, status=404)
    
    def delete(self, request, voucher_request_no):
        res = payment_processing.delete_voucher_request_by_id(voucher_request_no)
        
        if res["status"] == 'success':
            return Response(res, status=200 if res["data"]["rows_updated"] > 1 else 204)
        return Response(res, status=400)
    