import uuid
from django.db import models

# Create your models here.
class ProductType(models.Model):
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
        db_table = "tbmProductType"
        verbose_name = "Product Type"
        verbose_name_plural = "Product Type"
        
class ProductGroup(models.Model):
    # select FCSKID,FCCODE,FCNAME,FCNAME2 from PDGRP
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
        db_table = "tbmProductGroup"
        verbose_name = "Product Group"
        verbose_name_plural = "Product Group"
        
class Unit(models.Model):
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
        db_table = "tbmUnit"
        verbose_name = "Unit"
        verbose_name_plural = "Unit"


class Product(models.Model):
    # select p.FCSKID,p.FCTYPE,g.FCCODE,p.FCCODE,p.FCNAME,p.FCNAME2 from PROD p inner join PDGRP g on p.FCPDGRP=g.FCSKID where p.FCTYPE in ('1','5') order by p.FCCODE 
    id = models.UUIDField(primary_key=True, editable=False, verbose_name="PRIMARY KEY", default=uuid.uuid4)
    prod_type_id = models.ForeignKey(ProductType, verbose_name="Product Type ID", on_delete=models.SET_NULL, null=True)
    prod_group_id = models.ForeignKey(ProductGroup, verbose_name="Product Group ID", on_delete=models.SET_NULL, null=True)
    unit_id = models.ForeignKey(Unit, verbose_name="Unit ID", on_delete=models.SET_NULL, null=True)
    code = models.CharField(max_length=150, verbose_name="Code", unique=True, null=False)
    no = models.CharField(max_length=250, verbose_name="No", null=False)
    name = models.CharField(max_length=250, verbose_name="Name", null=False)
    std_pack = models.FloatField(verbose_name="STD Pack", blank=True, null=True, default="0.0")
    price = models.FloatField(verbose_name="Price", null=True, blank=True, default="0.0")
    description = models.TextField(verbose_name="Description",blank=True, null=True)
    img = models.ImageField(verbose_name="Image")
    is_active = models.BooleanField(verbose_name="Is Active", default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.code}"
    
    class Meta:
        db_table = "tbmProduct"
        verbose_name = "Product"
        verbose_name_plural = "Product"
        ordering = ("code","name")