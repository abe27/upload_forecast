import uuid
from django.db import models

from products.models import ProductType
from members.models import Corporation, Factory

BOOKING_TYPE = [
    ('F', 'Form Whs'),
    ('T', 'To Whs')
]

# Create your models here.
class EDIReviseType(models.Model):
    # select p.FCSKID,p.FCCODE,p.FCNAME,p.FCNAME2 from PRODTYPE p
    id = models.UUIDField(primary_key=True, editable=False, verbose_name="PRIMARY KEY", default=uuid.uuid4)
    code = models.IntegerField(verbose_name="Code", unique=True, blank=False, null=False)
    name = models.CharField(max_length=50, verbose_name="Name", unique=True, blank=False, null=False)
    description = models.TextField(verbose_name="Description",blank=True, null=True)
    is_active = models.BooleanField(verbose_name="Is Active", default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Rev.{str(self.code)}"
    
    def short_name(self):
        return f"Rev.{str(self.code)}"
    
    @classmethod
    def get_default_value_pk(cls):
        return cls.objects.get(code="0")[0].id
    
    class Meta:
        db_table = "tbmReviseType"
        verbose_name = "Revise Type"
        verbose_name_plural = "Revise Type"
        ordering = ("name", "description")
        

class RefType(models.Model):
    # select p.FCSKID,p.FCCODE,p.FCNAME,p.FCNAME2 from PRODTYPE p
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
        db_table = "tbmRefType"
        verbose_name = "Ref Type"
        verbose_name_plural = "Ref Type"
        
class Book(models.Model):
    # select FCSKID,FCREFTYPE,FCCODE,FCNAME,FCNAME2,FCPREFIX from BOOK
    id = models.UUIDField(primary_key=True, editable=False, verbose_name="PRIMARY KEY", default=uuid.uuid4)
    skid = models.CharField(max_length=50, verbose_name="Key", unique=True, blank=False, null=False)
    corporation_id = models.ForeignKey(Corporation, blank=True, null=True, on_delete=models.SET_NULL)
    order_type_id = models.ForeignKey(RefType, verbose_name="Type ID", on_delete=models.SET_NULL, null=True)
    filter_product_type = models.ManyToManyField(ProductType, blank=True, verbose_name="Filter Product Type ID")
    code = models.CharField(max_length=50, verbose_name="Code", blank=False, null=False)
    name = models.CharField(max_length=250, verbose_name="Name", blank=False, null=False)
    prefix = models.CharField(max_length=250, verbose_name="Prefix", blank=True, null=True)
    description = models.TextField(verbose_name="Description",blank=True, null=True)
    is_active = models.BooleanField(verbose_name="Is Active", default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.code}-{self.name}"
    
    @classmethod
    def get_default_value_pk(cls):
        return cls.objects.get(prefix="PR0002/")[0].id
    
    class Meta:
        db_table = "tbmBook"
        verbose_name = "Book"
        verbose_name_plural = "Book"
        
class BookDetail(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, verbose_name="PRIMARY KEY", default=uuid.uuid4)
    book_id = models.ForeignKey(Book, verbose_name="Book ID", on_delete=models.SET_NULL, null=True)
    factory_type = models.CharField(max_length=1, choices=BOOKING_TYPE,verbose_name="Book Ref")
    factory_id = models.OneToOneField(Factory, verbose_name="From Whs",blank=True, null=True, on_delete=models.SET_NULL)
    is_active = models.BooleanField(default=True, verbose_name="Is Active", blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.code}-{self.name}"
    
    class Meta:
        db_table = "tbmBookDetail"
        verbose_name = "Book Detail"
        verbose_name_plural = "Book Detail"
        
class ReviseBook(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, verbose_name="PRIMARY KEY", default=uuid.uuid4)
    ref_type_id = models.ForeignKey(RefType, verbose_name="Ref. Type ID", on_delete=models.SET_NULL, null=True)
    book_id = models.ForeignKey(Book, verbose_name="Book ID", on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=250, verbose_name="Name", unique=True,blank=False, null=False)
    description = models.TextField(verbose_name="Description",blank=True, null=True)
    is_active = models.BooleanField(default=True, verbose_name="Is Active", blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        db_table = "tbmReviseBook"
        verbose_name = "Revise Book"
        verbose_name_plural = "Revise Book"