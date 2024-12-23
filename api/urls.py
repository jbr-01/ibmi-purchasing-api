from django.urls import path
from .views import (CompanyListView, CompanyDetailView, ProjectListView, ProjectDetailView, 
    DepartmentListView, DepartmentDetailView, SupplierListView, SupplierDetailView,
    ItemListView, ItemDetailView, VoucherRequestListView, VoucherRequestDetailView)

urlpatterns = [
    path('companies/', CompanyListView.as_view(), name='company-list'),
    path('companies/<int:company_code>/', CompanyDetailView.as_view(), name='company-detail'),
    path('projects/', ProjectListView.as_view(), name='projects-list'),
    path('projects/<str:project_code>/', ProjectDetailView.as_view(), name='project-detail'),
    path('departments/', DepartmentListView.as_view(), name='departments-list'),
    path('departments/<int:department_code>/', DepartmentDetailView.as_view(), name='department-detail'),
    path('suppliers/', SupplierListView.as_view(), name='suppliers-list'),
    path('suppliers/<str:supplier_code>/', SupplierDetailView.as_view(), name='supplier-detail'),
    path('items/', ItemListView.as_view(), name='items-list'),
    path('items/<str:item_code>/', ItemDetailView.as_view(), name='item-detail'),
    path('payment_processing/voucher_request/', VoucherRequestListView.as_view(), name='voucher-request-list'),
    path('payment_processing/voucher_request/<str:voucher_request_no>/', VoucherRequestDetailView.as_view(), name='voucher-request-detail'),
]
