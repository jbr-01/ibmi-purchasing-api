from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Company(models.Model):

    company_code = models.IntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(99)])
    company_name = models.CharField(max_length=45)
    company_initials = models.CharField(max_length=5)
    company_tin = models.CharField(max_length=18)
    company_contact_no = models.CharField(max_length=8)
    company_address = models.CharField(max_length=90)
    
    def __str__(self):
        return self.company_code

class Project(models.Model):
    project_code = models.CharField(max_length=3)
    company_initials = models.CharField(max_length=5)
    company_tin = models.CharField(max_length=18)
    company_contact_no = models.CharField(max_length=8)
    company_address = models.CharField(max_length=90)

    def __str__(self):
        return self.project_code
    
class Departments(models.Model):
    department_code = models.IntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(99)])
    department_name = models.CharField(max_length=20)

    def __str__(self):
        return self.department_code
    
class Suppliers(models.Model):
    supplier_code = models.CharField(max_length=4)

    def __str__(self):
        return self.supplier_code
    
class Items(models.Model):
    account_code = models.CharField(max_length=14)

    def __str__(self):
        return self.account_code
    
class VoucherRequestGet(models.Model):
    voucher_request_no = models.CharField(max_length=12)
    
    def __str__(self):
        return self.voucher_request_no
    
class VoucherSupplier(models.Model):
    code = models.CharField(max_length=4)
    name = models.CharField(max_length=50)
    tin = models.CharField(max_length=20)

    def __str__(self):
        return self.name
    
class Voucher(models.Model):
    prs_username = models.CharField(max_length=10)
    voucher_request_no = models.CharField(max_length=12)
    branch_code = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)])
    company_code = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(99)])
    date_prepared = models.DateField()
    time_prepared = models.TimeField()
    supplier = models.ForeignKey(VoucherSupplier, on_delete=models.CASCADE, related_name='vouchers')
    total_amount = models.DecimalField(max_digits=15, decimal_places=2)
    project_code = models.CharField(max_length=3)

    def __str__(self):
        return self.voucher_request_no

class VoucherLine(models.Model):
    voucher = models.ForeignKey(Voucher, on_delete=models.CASCADE, related_name='lines')
    account_code = models.CharField(max_length=14)
    amount = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return f"{self.account_code} - {self.amount}"

class VoucherItem(models.Model):
    line = models.ForeignKey(VoucherLine, on_delete=models.CASCADE, related_name='items')
    quantity = models.PositiveIntegerField()
    unit = models.CharField(max_length=4)
    description = models.CharField(max_length=30)
    amount = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return self.description
    