from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .db_utils import (companies, projects, departments, suppliers, items, payment_processing)
from .serializers import (CompanySerializer, ProjectSerializer, DepartmentSerializer, SuppliersSerializer,
    ItemsSerializer, VoucherRequestGetSerializer, VoucherSerializer)

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
        compcd = {"company_code": company_code }
        serializer = CompanySerializer(data=compcd)
        if serializer.is_valid():
            company = companies.fetch_company_by_id(company_code)
            if company:
                return Response(company)
            return Response({
                "error": "COMPANY_NOT_FOUND",
                "message": f"No company found with code '{company_code}'",
            }, status=404)
            
        return Response({
            "error": "VALIDATION_ERROR",
            "message": serializer.errors,
        }, status=400)

class ProjectListView(APIView):
    def get(self, request):
        projectsList = projects.fetch_all_projects()
        return Response(projectsList)

class ProjectDetailView(APIView):
    def get(self, request, project_code):
        projcd = {"project_code": project_code }
        serializer = ProjectSerializer(data=projcd)
        if serializer.is_valid():
            project = projects.fetch_project_by_id(project_code)
            if project:
                return Response(project)
            return Response({
                "error": "PROJECT_NOT_FOUND",
                "message": f"No project found with code '{project_code}'",
            }, status=404)
            
        return Response({
            "error": "VALIDATION_ERROR",
            "message": serializer.errors,
        }, status=400)
        
    
class DepartmentListView(APIView):
    def get(self, request):
        departmentsList = departments.fetch_all_departments()
        return Response(departmentsList)

class DepartmentDetailView(APIView):
    def get(self, request, department_code):
        compcd = {"department_code": department_code }
        serializer = DepartmentSerializer(data=compcd)
        if serializer.is_valid():
            department = departments.fetch_department_by_id(department_code)
            if department:
                return Response(department)
            return Response({
                "error": "DEPARTMENT_NOT_FOUND",
                "message": f"No department found with code '{department_code}'",
            }, status=404)
            
        return Response({
            "error": "VALIDATION_ERROR",
            "message": serializer.errors,
        }, status=400)
        
class SupplierListView(APIView):
    def get(self, request):
        suppliersList = suppliers.fetch_all_suppliers()
        return Response(suppliersList)

class SupplierDetailView(APIView):
    def get(self, request, supplier_code):
        suppCode = {"supplier_code": supplier_code }
        serializer = SuppliersSerializer(data=suppCode)
        if serializer.is_valid():
            supplier = suppliers.fetch_supplier_by_id(supplier_code)
            if supplier:
                return Response(supplier)
            return Response({
                "error": "SUPPLIER_NOT_FOUND",
                "message": f"No Supplier found with code '{supplier_code}'",
            }, status=404)
            
        return Response({
            "error": "VALIDATION_ERROR",
            "message": serializer.errors,
        }, status=400)

class ItemListView(APIView):
    def get(self, request):
        itemsList = items.fetch_all_items()
        return Response(itemsList)

class ItemDetailView(APIView):
    def get(self, request, account_code):
        acctCode = {"account_code": account_code }
        serializer = ItemsSerializer(data=acctCode)
        if serializer.is_valid():
            item = items.fetch_item_by_id(account_code)
            if item:
                return Response(item)
            return Response({
                "error": "ITEM_NOT_FOUND",
                "message": f"No Item found with code '{account_code}'",
            }, status=404)
            
        return Response({
            "error": "VALIDATION_ERROR",
            "message": serializer.errors,
        }, status=400)
        
class VoucherRequestDetailView(APIView):
    def get(self, request, voucher_request_no):
        vrNo = {"voucher_request_no": voucher_request_no }
        serializer = VoucherRequestGetSerializer(data=vrNo)
        if serializer.is_valid():
            vr = payment_processing.fetch_voucher_request_by_id(voucher_request_no)
            if vr:
                if not vr.get("data"):
                    return Response({
                        "error": "VOUCHER_REQUEST_NOT_FOUND",
                        "message": f"No Voucher Request found with No. '{voucher_request_no}'",
                    }, status=404)
                return Response(vr)
            return Response({
                "error": "VOUCHER_REQUEST_NOT_FOUND",
                "message": f"No Voucher Request found with No. '{voucher_request_no}'",
            }, status=404)
            
        return Response({
            "error": "VALIDATION_ERROR",
            "message": serializer.errors,
        }, status=400)
        
    def post(self, request, *args, **kwargs):
        data = request.data.get("voucher_request")
        serializer = VoucherSerializer(data=data)
        if serializer.is_valid():
            res = payment_processing.add_voucher_request(data)
            if res["status"] == "success":
                return Response(res, status=201)
            return Response(res, status=400)
        
        return Response({
            "error": "VALIDATION_ERROR",
            "message": serializer.errors,
        }, status=400)
        
    def delete(self, request, voucher_request_no):
        vrNo = {"voucher_request_no": voucher_request_no }
        serializer = VoucherRequestGetSerializer(data=vrNo)
        if serializer.is_valid():
            res = payment_processing.cancel_voucher_request_by_id(voucher_request_no)
            if res["status"] == "success":
                return Response(res, status=200)
            return Response(res, status=400)
        
        return Response({
            "error": "VALIDATION_ERROR",
            "message": serializer.errors,
        }, status=400)
        