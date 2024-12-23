from django.db import models

# Create your models here.

class Company(models.Model):
    company_code = models.IntegerField(default=0) 
    company_name = models.CharField(max_length=45)
    company_initials = models.CharField(max_length=5)
    company_tin = models.CharField(max_length=18)
    company_contact_no = models.CharField(max_length=8)
    company_address = models.CharField(max_length=90)
    
    def __str__(self):
        return self.company_code
    
    # def clean(self):
    #     print(self)
    #     if self.name == 'admin' and self.age < 30:
    #         raise ValidationError("Admin must be at least 30 years old.")

class Project(models.Model):
    # project_code = models.IntegerField(default=0) 
    project_code = models.CharField(max_length=3)
    company_initials = models.CharField(max_length=5)
    company_tin = models.CharField(max_length=18)
    company_contact_no = models.CharField(max_length=8)
    company_address = models.CharField(max_length=90)

    def __str__(self):
        return self.project_code
    
class Departments(models.Model):
    department_code = models.IntegerField(default=0)
    department_name = models.CharField(max_length=20)

    def __str__(self):
        return self.department_code
    
class Suppliers(models.Model):
    supplier_code = models.CharField(max_length=4)

    def __str__(self):
        return self.supplier_code
    
class Items(models.Model):
    item_code = models.CharField(max_length=8)

    def __str__(self):
        return self.item_code
    
class VoucherRequest(models.Model):
    voucher_request_no = models.CharField(max_length=12, unique=True)
    reference_no = models.CharField(max_length=20)
    particulars_total_amount = models.DecimalField(max_digits=15, decimal_places=2)
    
    def __str__(self):
        return f"{self.voucher_request_no} - {self.reference_no}"
    
    # item_code = models.CharField(max_length=8)

    # def __str__(self):
    #     return self.item_code

class VoucherRequestHeader(models.Model):
    # voucher_request = models.OneToOneField(
    #     VoucherRequest, on_delete=models.CASCADE, related_name="header"
    # )
    voucher_request = models.ForeignKey(VoucherRequest, on_delete=models.CASCADE)
    company_code = models.PositiveIntegerField()
    branch = models.PositiveIntegerField()
    project_code = models.CharField(max_length=3)
    date_prepared = models.DateField()
    supplier_code = models.CharField(max_length=4)
    supplier_name = models.CharField(max_length=35)
    total_amount = models.DecimalField(max_digits=15, decimal_places=2)
    voucher_type = models.CharField(max_length=1)

    # def __str__(self):
    #     return f"Header for {self.voucher_request}"


class VoucherRequestDetail(models.Model):
    # voucher_request = models.ForeignKey(
    #     VoucherRequest, on_delete=models.CASCADE, related_name="detail"
    # )
    voucher_request = models.ForeignKey(VoucherRequest, on_delete=models.CASCADE)
    account_code = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=15, decimal_places=2)

    # def __str__(self):
    #     return f"Detail {self.account_code} - {self.amount}"

class VoucherRequestParticular(models.Model):
    # voucher_request = models.ForeignKey(
    #     VoucherRequest, on_delete=models.CASCADE, related_name="particulars"
    # )
    voucher_request = models.ForeignKey(VoucherRequest, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    item_description = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=15, decimal_places=2)

    # def __str__(self):
    #     return f"Particular {self.item_description} - {self.amount}"
