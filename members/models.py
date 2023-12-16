import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


ON_MONTH_LIST = [
    ('0', '-'),
    ('1', 'January'), 
    ('2', 'February'), 
    ('3', 'March'), 
    ('4', 'April'), 
    ('5', 'May'), 
    ('6', 'June'), 
    ('7', 'July'), 
    ('8', 'August'), 
    ('9', 'September'),
    ('10', 'October'),
    ('11', 'November'),
    ('12', 'December'),]

ON_YEAR_LIST = [
    ('2023','2023'),
    ('2024','2024'),
    ('2025','2025'),
    ('2026','2026'),
    ('2027','2027'),
    ('2028','2028'),
    ('2029','2029'),
    ('2030','2030'),
]

# Create your models here.
class Corporation(models.Model):
    # select p.FCCODE,p.FCNAME,p.FCNAME2 from PRODTYPE p
    id = models.UUIDField(primary_key=True, editable=False, verbose_name="PRIMARY KEY", default=uuid.uuid4)
    code = models.CharField(max_length=50, verbose_name="Code", unique=True, blank=False, null=False)
    name = models.CharField(max_length=250, verbose_name="Name", blank=False, null=False)
    description = models.TextField(verbose_name="Description",blank=True, null=True)
    is_active = models.BooleanField(verbose_name="Is Active", default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "tbmCorporation"
        verbose_name = "Corporation"
        verbose_name_plural = "Corporation"
        
class Factory(models.Model):
    # select p.FCSKID,p.FCCODE,p.FCNAME,p.FCNAME2 from UM p
    id = models.UUIDField(primary_key=True, editable=False, verbose_name="PRIMARY KEY", default=uuid.uuid4)
    code = models.CharField(max_length=50, verbose_name="Code", unique=True,blank=False, null=False)
    name = models.CharField(max_length=250, verbose_name="Name", blank=False, null=False)
    description = models.TextField(verbose_name="Description",blank=True, null=True)
    is_active = models.BooleanField(verbose_name="Is Active", default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "tbmFactory"
        verbose_name = "Factory"
        verbose_name_plural = "Factory"
                
class Section(models.Model):
    # select FCSKID,FCCODE,FCNAME,FCNAME2 from SECT
    id = models.UUIDField(primary_key=True, editable=False, verbose_name="PRIMARY KEY", default=uuid.uuid4)
    code = models.CharField(max_length=50, verbose_name="Code", unique=True,blank=False, null=False)
    name = models.CharField(max_length=250, verbose_name="Name", blank=False, null=False)
    description = models.TextField(verbose_name="Description",blank=True, null=True)
    is_active = models.BooleanField(verbose_name="Is Active", default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "tbmSection"
        verbose_name = "Section"
        verbose_name_plural = "Section"
        
class Position(models.Model):
    # select FCSKID,FCCODE,FCNAME,FCNAME2 from SECT
    id = models.UUIDField(primary_key=True, editable=False, verbose_name="PRIMARY KEY", default=uuid.uuid4)
    code = models.CharField(max_length=50, verbose_name="Code", unique=True,blank=False, null=False)
    name = models.CharField(max_length=250, verbose_name="Name", blank=False, null=False)
    description = models.TextField(verbose_name="Description",blank=True, null=True)
    is_active = models.BooleanField(verbose_name="Is Active", default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "tbmPosition"
        verbose_name = "Position"
        verbose_name_plural = "Position"

class Department(models.Model):
    # select FCSKID,FCCODE,FCNAME,FCNAME2 from DEPT
    id = models.UUIDField(primary_key=True, editable=False, verbose_name="PRIMARY KEY", default=uuid.uuid4)
    code = models.CharField(max_length=50, verbose_name="Code", unique=True,blank=False, null=False)
    name = models.CharField(max_length=250, verbose_name="Name", blank=False, null=False)
    description = models.TextField(verbose_name="Description",blank=True, null=True)
    is_active = models.BooleanField(verbose_name="Is Active", default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "tbmDepartment"
        verbose_name = "Department"
        verbose_name_plural = "Department"
        
class Employee(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, verbose_name="PRIMARY KEY", default=uuid.uuid4)
    corporation_id = models.ForeignKey(Corporation, blank=True, null=True, on_delete=models.SET_NULL)
    code = models.CharField(max_length=50, verbose_name="Code", unique=True,blank=False, null=False)
    name = models.CharField(max_length=250, verbose_name="Name", blank=False, null=False)
    description = models.TextField(verbose_name="Description",blank=True, null=True)
    is_active = models.BooleanField(verbose_name="Is Active", default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.code}-{self.name}"
    
    class Meta:
        db_table = "tbmFormulaEmployee"
        verbose_name = "Formula Employee"
        verbose_name_plural = "Formula Employee"
        

class LineNotification(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, verbose_name="PRIMARY KEY", default=uuid.uuid4)
    token = models.CharField(max_length=50,verbose_name="Token Key", unique=True)
    name = models.CharField(max_length=255, verbose_name="Group Name")
    description = models.TextField(verbose_name="Description",blank=True, null=True)
    is_active = models.BooleanField(verbose_name="Is Active", default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "tbmLineNotification"
        verbose_name = "Line Notification"
        verbose_name_plural = "Line Notification"

class Supplier(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, verbose_name="PRIMARY KEY", default=uuid.uuid4)
    code = models.CharField(max_length=150, verbose_name="Code",unique=True,blank=False, null=False)
    name = models.CharField(max_length=250, verbose_name="Name", blank=False, null=False)
    description = models.TextField(verbose_name="Description",blank=True, null=True)
    is_active = models.BooleanField(verbose_name="Is Active", default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.code}-{self.name}"
    
    class Meta:
        db_table = "tbmSupplier"
        verbose_name = "Supplier"
        verbose_name_plural = "Supplier"
        
class ManagementUser(AbstractUser):
    formula_user_id = models.ForeignKey(Employee, verbose_name="Formula User ID", blank=True, null=True, on_delete=models.SET_NULL)
    factory_id = models.ForeignKey(Factory, blank=True, verbose_name="Factory ID",null=True, on_delete=models.SET_NULL)
    supplier_id = models.ManyToManyField(Supplier, blank=True, verbose_name="Supplier ID",related_name='SetSupplier')
    department_id = models.ForeignKey(Department, blank=True, verbose_name="Department ID",null=True, on_delete=models.SET_NULL)
    position_id = models.ForeignKey(Position, blank=True, verbose_name="Position ID",null=True, on_delete=models.SET_NULL)
    section_id = models.ForeignKey(Section, blank=True, verbose_name="Section ID",null=True, on_delete=models.SET_NULL)
    line_notification_id = models.ForeignKey(LineNotification, blank=True, verbose_name="Line Notification ID",null=True, on_delete=models.SET_NULL)
    description = models.TextField(verbose_name="Description",blank=True, null=True)
    avatar_url = models.ImageField(verbose_name="Avatar Image",blank=True, null=True)
    signature_img = models.ImageField(verbose_name="Signature Image",blank=True, null=True)
    is_approve = models.BooleanField(verbose_name="Is Approve", default=False)
    is_issue = models.BooleanField(verbose_name="Is Issue", default=False)
    is_active = models.BooleanField(verbose_name="Is Active", default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return super().__str__()
    
    class Meta:
        db_table = "ediUser"
        verbose_name = "User"
        verbose_name_plural = "User"
        
class PlanningForecast(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, verbose_name="PRIMARY KEY", default=uuid.uuid4)
    plan_day = models.IntegerField(blank=True, null=True, verbose_name="Day", default="1")
    plan_month = models.CharField(max_length=2,choices=ON_MONTH_LIST, blank=True, null=True, verbose_name="On Month")
    plan_year = models.IntegerField(blank=True, null=True, verbose_name="On Year")
    plan_qty = models.IntegerField(verbose_name="Planning Qty",blank=True, null=True, default="0")
    revise_plan_qty = models.IntegerField(verbose_name="Revise Qty",blank=True, null=True, default="0")
    is_active = models.BooleanField(verbose_name="Is Active", default=False,blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{ON_MONTH_LIST[int(self.plan_month)][1]} {self.plan_year}"
    
    class Meta:
        db_table = "tbmPlanningForecast"
        verbose_name = "PlanningForecast"
        verbose_name_plural = "Planning Forecast"
        ordering = ("plan_year","plan_month", )
        
class ReportApproveByUser(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, verbose_name="PRIMARY KEY", default=uuid.uuid4)
    user_id = models.ForeignKey(ManagementUser, verbose_name="User ID", on_delete=models.CASCADE)
    is_active = models.BooleanField(verbose_name="Is Active", default=False,blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.user_id.username
    
    class Meta:
        db_table = "tbmReportApproveByUser"
        verbose_name = "ReportApproveByUser"
        verbose_name_plural = "Report Approve By User"
        
class ReportIssueByUser(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, verbose_name="PRIMARY KEY", default=uuid.uuid4)
    user_id = models.ForeignKey(ManagementUser, verbose_name="User ID", on_delete=models.CASCADE)
    is_active = models.BooleanField(verbose_name="Is Active", default=False,blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.user_id.username
    
    class Meta:
        db_table = "tbmReportIssueByUser"
        verbose_name = "Report Issue ByUser"
        verbose_name_plural = "Report Issue By User"
        

class OrganizationApprovePDS(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, verbose_name="PRIMARY KEY", default=uuid.uuid4)
    approve_by_id = models.ForeignKey(ReportApproveByUser, blank=True, verbose_name="Approve By ID",null=True, on_delete=models.SET_NULL)
    issue_by_id = models.ForeignKey(ReportIssueByUser, blank=True, verbose_name="Issue By ID",null=True, on_delete=models.SET_NULL)
    is_active = models.BooleanField(verbose_name="Is Active", default=False,blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.approve_by_id
    
    class Meta:
        db_table = "tbmOrganizationApprovePDS"
        verbose_name = "Organize Approve PDS"
        verbose_name_plural = "Organize Approve PDS"
        # ordering = ("plan_year","plan_month", )

class JasperReportServer(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, verbose_name="PRIMARY KEY", default=uuid.uuid4)
    server_name = models.CharField(max_length=255, verbose_name="Server Name")
    server_url = models.CharField(max_length=255, verbose_name="Server URL")
    is_active = models.BooleanField(verbose_name="Is Active", default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return self.server_name
    
    class Meta:
        db_table = "tbmServerReport"
        verbose_name = "Server Report PDS"
        verbose_name_plural = "Server Report PDS"
        
class UserErrorLog(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, verbose_name="PRIMARY KEY", default=uuid.uuid4)
    user_id = models.ForeignKey(ManagementUser, verbose_name="User ID", on_delete=models.CASCADE, blank=True)
    remark = models.TextField(verbose_name="หมายเหตุ")
    is_status = models.BooleanField(verbose_name="Success", default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    
    # def __str__(self):
    #     return self.user_id
    
    class Meta:
        db_table = "tbmLoggingReport"
        verbose_name = "Logging Report Handle"
        verbose_name_plural = "Logging Report Handle"
        ordering = ("-updated_on",)