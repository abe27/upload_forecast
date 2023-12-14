from django.db import models

# Create your models here.
class DEPT(models.Model):
    FCSKID = models.CharField(max_length=8, db_column="FCSKID",  primary_key=True, editable=False)
    FCCODE = models.CharField(max_length=30, db_column="FCCODE")
    FCNAME = models.CharField(max_length=30, db_column="FCNAME")
    
    def __str__(self):
        return self.FCSKID
    
    class Meta:
        db_table = "DEPT"
        app_label = "formula_vcst"
        
class SECT(models.Model):
    FCSKID = models.CharField(max_length=8, db_column="FCSKID", primary_key=True, editable=False)
    FCCODE = models.CharField(max_length=30, db_column="FCCODE")
    FCNAME = models.CharField(max_length=30, db_column="FCNAME")
    
    def __str__(self):
        return self.FCSKID
    
    class Meta:
        db_table = "SECT"
        app_label = "formula_vcst"
        
class JOB(models.Model):
    FCSKID = models.CharField(max_length=8, db_column="FCSKID", primary_key=True, editable=False)
    FCCODE = models.CharField(max_length=30, db_column="FCCODE")
    FCNAME = models.CharField(max_length=30, db_column="FCNAME")
    
    def __str__(self):
        return self.FCSKID
    
    class Meta:
        db_table = "JOB"
        app_label = "formula_vcst"
        
class UM(models.Model):
    FCSKID = models.CharField(max_length=8, db_column="FCSKID", primary_key=True, editable=False)
    FCCODE = models.CharField(max_length=30, db_column="FCCODE")
    FCNAME = models.CharField(max_length=30, db_column="FCNAME")
    
    def __str__(self):
        return self.FCSKID
    
    class Meta:
        db_table = "UM"
        app_label = "formula_vcst"
        
class BOOK(models.Model):
    FCSKID = models.CharField(max_length=8, db_column="FCSKID", primary_key=True, editable=False)
    FCCODE = models.CharField(max_length=30, db_column="FCCODE")
    FCNAME = models.CharField(max_length=30, db_column="FCNAME")
    FCREFTYPE = models.CharField(max_length=30, db_column="FCREFTYPE",blank=True, null=True)
    FCPREFIX = models.CharField(max_length=30, db_column="FCPREFIX",blank=True, null=True)
    
    def __str__(self):
        return self.FCSKID
    
    class Meta:
        db_table = "BOOK"
        app_label = "formula_vcst"
        
class COOR(models.Model):
    FCSKID = models.CharField(max_length=8, db_column="FCSKID",primary_key=True, editable=False)
    FCCODE = models.CharField(max_length=30, db_column="FCCODE")
    FCNAME = models.CharField(max_length=30, db_column="FCNAME")
    
    def __str__(self):
        return self.FCSKID
    
    class Meta:
        db_table = "COOR"
        app_label = "formula_vcst"
        
class CORP(models.Model):
    FCSKID = models.CharField(max_length=8, db_column="FCSKID",primary_key=True, editable=False)
    FCCODE = models.CharField(max_length=30, db_column="FCCODE")
    FCNAME = models.CharField(max_length=30, db_column="FCNAME")
    
    def __str__(self):
        return self.FCSKID
    
    class Meta:
        db_table = "CORP"
        app_label = "formula_vcst"
        
class PROD(models.Model):
    FCSKID = models.CharField(max_length=8, db_column="FCSKID",primary_key=True, editable=False)
    FCCODE = models.CharField(max_length=30, db_column="FCCODE")
    FCNAME = models.CharField(max_length=30, db_column="FCNAME")
    FCPDGRP = models.CharField(max_length=30, db_column="FCPDGRP")
    FCTYPE = models.CharField(max_length=30, db_column="FCTYPE")
    FNPRICE = models.FloatField(db_column="FNPRICE", blank=True, null=True, default="0.0")
    FNSTDCOST = models.FloatField(db_column="FNSTDCOST", blank=True, null=True, default="0.0")
    
    def __str__(self):
        return self.FCSKID
    class Meta:
        db_table = "PROD"
        app_label = "formula_vcst"
        

class EMPLOYEE(models.Model):
    FCSKID = models.CharField(max_length=8, db_column="FCSKID",primary_key=True, editable=False)
    FCCODE = models.CharField(max_length=30, db_column="FCCODE")
    FCNAME = models.CharField(max_length=30, db_column="FCNAME")
    
    def __str__(self):
        return self.FCCODE
    
    class Meta:
        db_table = "EMPL"
        app_label = "formula_vcst"
        
class OrderH(models.Model):
    FCDATASER = models.CharField(max_length=4, db_column="FCDATASER", default="$$$9",blank=True, null=True,)
    FCSKID = models.CharField(max_length=8, db_column="FCSKID",primary_key=True, editable=False)
    FCLUPDAPP = models.CharField(max_length=2, db_column="FCLUPDAPP", blank=True, null=True, default="$/")
    FCRFTYPE = models.CharField(max_length=1, db_column="FCRFTYPE", default="w", blank=True, null=True)### Reference
    FCREFTYPE = models.CharField(max_length=2, db_column="FCREFTYPE")### Reference PR/PO
    FCCORP = models.CharField(max_length=8, db_column="FCCORP", default="H2ZFEv02", blank=True, null=True)
    FCBRANCH = models.CharField(max_length=8, db_column="FCBRANCH", default="H2Z2kf01", blank=True, null=True)
    FCDEPT = models.CharField(max_length=8, db_column="FCDEPT")### Reference DEPT
    FCSECT = models.CharField(max_length=8, db_column="FCSECT")### Reference SECT
    FCJOB = models.CharField(max_length=8, db_column="FCJOB", default="H2ZFfr02", blank=True, null=True)
    FCSTEP = models.CharField(max_length=1, db_column="FCSTEP", default="1", blank=True, null=True)
    FCBOOK = models.CharField(max_length=8, db_column="FCBOOK", default="JIXeqL01", blank=True, null=True)
    FCCODE = models.CharField(max_length=30, db_column="FCCODE")
    FCREFNO = models.CharField(max_length=35, db_column="FCREFNO")
    FCVATISOUT = models.CharField(max_length=1, db_column="FCVATISOUT", default="Y", blank=True, null=True)
    FCVATTYPE = models.CharField(max_length=1, db_column="FCVATTYPE", default="1", blank=True, null=True)
    FCCOOR = models.CharField(max_length=8, db_column="FCCOOR")### Reference COOR
    FCCREATEBY = models.CharField(max_length=8, db_column="FCCREATEBY", blank=True, null=True)### Reference EMP
    FCCORRECTB = models.CharField(max_length=8, db_column="FCCORRECTB", default="$/")### Reference
    FCEAFTERR = models.CharField(max_length=1, db_column="FCEAFTERR", default="E",blank=True, null=True)
    FCPROJ = models.CharField(max_length=8, db_column="FCPROJ", default="x/•ู((()",blank=True, null=True)
    FCAPPROVEB = models.CharField(max_length=8, db_column="FCAPPROVEB", blank=True, null=True)
    FCDELICOOR = models.CharField(max_length=8, db_column="FCDELICOOR", default="",blank=True, null=True)
    FCCREATEAP = models.CharField(max_length=8, db_column="FCCREATEAP", default="$/",blank=True, null=True)
    FCISPDPART = models.CharField(max_length=1, db_column="FCISPDPART", default="",blank=True, null=True)
    FDDATE = models.DateField(db_column="FDDATE")
    FDDUEDATE = models.DateTimeField(db_column="FDDUEDATE", auto_now=True)
    FDRECEDATE = models.DateField(db_column="FDRECEDATE", auto_now=True)
    FTDATETIME = models.DateTimeField(db_column="FTDATETIME", auto_now=True)
    FDAPPROVE = models.DateField(db_column="FDAPPROVE", auto_now=True)
    FTLASTUPD = models.DateTimeField(db_column="FTLASTUPD", auto_now=True)
    FDREQDATE = models.DateField(db_column="FDREQDATE", auto_now=True)
    FNAMT = models.FloatField(db_column="FNAMT", default="0.0", blank=True, null=True)
    FNAMT2 = models.FloatField(db_column="FNAMT2", default="0.0", blank=True, null=True)
    FNVATRATE = models.FloatField(db_column="FNVATRATE", default="7.0", blank=True, null=True)
    FNVATAMT = models.FloatField(db_column="FNVATAMT", default="0.0", blank=True, null=True)
    FNCREDTERM = models.FloatField(db_column="FNCREDTERM", default="0.0", blank=True, null=True)
    FNAMTKE = models.FloatField(db_column="FNAMTKE", default="0.0", blank=True, null=True)
    FNVATAMTKE = models.FloatField(db_column="FNVATAMTKE", default="0.0", blank=True, null=True)
    FNXRATE = models.FloatField(db_column="FNXRATE", default="0.0", blank=True, null=True)
    
    def __str__(self):
        return self.FCCODE
    
    class Meta:
        db_table = "ORDERH"
        app_label = "formula_vcst"
        
class OrderI(models.Model):
    FCBRANCH= models.CharField(max_length=8, db_column="FCBRANCH", default="H2Z2kf01", blank=True, null=True)
    FCCOOR = models.CharField(max_length=8, db_column="FCCOOR")### Reference
    FCCORP = models.CharField(max_length=8, db_column="FCCORP", default="H2ZFEv02", blank=True, null=True)
    FCCREATEAP = models.CharField(max_length=2, db_column="FCCREATEAP", default="$/", blank=True, null=True)
    FCDATASER = models.CharField(max_length=4, db_column="FCDATASER", default="$$$+", blank=True, null=True)
    FCDEPT = models.CharField(max_length=8, db_column="FCDEPT")## Refrence
    FCEAFTERR = models.CharField(max_length=1, db_column="FCEAFTERR", default="E", blank=True, null=True)
    FCGVPOLICY = models.CharField(max_length=1, db_column="FCGVPOLICY", default="1", blank=True, null=True)
    FCJOB = models.CharField(max_length=8, db_column="FCJOB", default="H2ZFfr02", blank=True, null=True)
    FCLUPDAPP = models.CharField(max_length=2, db_column="FCLUPDAPP", default="$/", blank=True, null=True)
    FCORDERH = models.CharField(max_length=8, db_column="FCORDERH")## refrence ORDERH
    FCPROD = models.CharField(max_length=8, db_column="FCPROD")### ref prod
    FCPRODTYPE = models.CharField(max_length=1, db_column="FCPRODTYPE")### ref product type
    FCPROJ = models.CharField(max_length=8, db_column="FCPROJ", default="H2ZFfQ02", blank=True, null=True)
    FCREFPDTYP = models.CharField(max_length=1, db_column="FCREFPDTYP", default="P", blank=True, null=True)
    FCREFTYPE = models.CharField(max_length=2, db_column="FCREFTYPE")### ref PR/PO
    FCSECT = models.CharField(max_length=8, db_column="FCSECT")### ref section
    FCSEQ = models.CharField(max_length=4, db_column="FCSEQ")### 001
    FCSHOWCOMP = models.CharField(max_length=1, db_column="FCSHOWCOMP", blank=True, null=True)
    FCSKID = models.CharField(max_length=8, db_column="FCSKID",primary_key=True, editable=False)
    FCSTEP = models.CharField(max_length=1, db_column="FCSTEP", default="1", blank=True, null=True)
    FCSTUM = models.CharField(max_length=8, db_column="FCSTUM")### ref unit
    FCUM = models.CharField(max_length=8, db_column="FCUM")### ref unit
    FCUMSTD = models.CharField(max_length=8, db_column="FCUMSTD")### ref unit
    FCVATISOUT = models.CharField(max_length=1, db_column="FCVATISOUT", default="Y", blank=True, null=True)
    FCVATTYPE = models.CharField(max_length=1, db_column="FCVATTYPE", default="1", blank=True, null=True)
    FCWHOUSE = models.CharField(max_length=8, db_column="FCWHOUSE", default="H2u7qN02", blank=True, null=True)
    FDDATE = models.DateField(db_column="FDDATE", blank=True, null=True)
    FDDELIVERY = models.DateField(db_column="FDDELIVERY", blank=True, null=True)
    FMREMARK = models.TextField(db_column="FMREMARK", blank=True, null=True)
    FNBACKQTY = models.FloatField(db_column="FNBACKQTY", default="0.0", blank=True, null=True)
    FNPRICE = models.FloatField(db_column="FNPRICE", default="0.0", blank=True, null=True)
    FNPRICEKE = models.FloatField(db_column="FNPRICEKE", default="0.0", blank=True, null=True)
    FNQTY = models.FloatField(db_column="FNQTY", default="0.0", blank=True, null=True)
    FNUMQTY = models.FloatField(db_column="FNUMQTY", default="1", blank=True, null=True)
    FNVATAMT = models.FloatField(db_column="FNVATAMT", default="0.0", blank=True, null=True)
    FNVATRATE = models.FloatField(db_column="FNVATRATE", default="7.0", blank=True, null=True)
    FNXRATE = models.FloatField(db_column="FNXRATE", default="1.0", blank=True, null=True)
    FTDATETIME = models.DateTimeField(db_column="FTDATETIME", auto_now=True)
    FTLASTUPD = models.DateTimeField(db_column="FTLASTUPD", auto_now=True)
    
    def __str__(self):
        return self.FCSKID
    
    class Meta:
        db_table = "ORDERI"
        app_label = "formula_vcst"
        
class NoteCut(models.Model):
    FCAPPNAME = models.CharField(max_length=128, db_column="FCAPPNAME", blank=True, null=True)
    FCBRANCH = models.CharField(max_length=8, db_column="FCBRANCH", blank=True, null=True,default="H2Z2kf01")
    FCCHILDH = models.CharField(max_length=8, db_column="FCCHILDH", blank=True, null=True)### ref ORDERH PR record
    FCCHILDI = models.CharField(max_length=8, db_column="FCCHILDI", blank=True, null=True)### ref ORDERI PR record
    FCCHILDTYP = models.CharField(max_length=2, db_column="FCCHILDTYP", blank=True, null=True, default="PR")
    FCCORP = models.CharField(max_length=8, db_column="FCCORP", blank=True, null=True, default="H2ZFEv02")
    FCCORRECTB = models.CharField(max_length=8, db_column="FCCORRECTB", blank=True, null=True)
    FCCREATEAP = models.CharField(max_length=2, db_column="FCCREATEAP", blank=True, null=True, default="$/")
    FCCREATEBY = models.CharField(max_length=8, db_column="FCCREATEBY", blank=True, null=True)
    FCCREATETY = models.CharField(max_length=1, db_column="FCCREATETY", blank=True, null=True)
    FCCUACC = models.CharField(max_length=128, db_column="FCCUACC", blank=True, null=True)
    FCDATAIMP = models.CharField(max_length=1, db_column="FCDATAIMP", blank=True, null=True)
    FCDATASER = models.CharField(max_length=4, db_column="FCDATASER", blank=True, null=True, default="$$$+")
    FCEAFTERR = models.CharField(max_length=1, db_column="FCEAFTERR", blank=True, null=True, default="E")
    FCLUPDAPP = models.CharField(max_length=2, db_column="FCLUPDAPP", blank=True, null=True, default="$/")
    FCMASTERH = models.CharField(max_length=8, db_column="FCMASTERH", blank=True, null=True)### ref ORDERH PO record
    FCMASTERI = models.CharField(max_length=8, db_column="FCMASTERI", blank=True, null=True)### ref ORDERH PO record
    FCMASTERTY = models.CharField(max_length=2, db_column="FCMASTERTY", blank=True, null=True, default="PO")
    FCORGCODE = models.CharField(max_length=128, db_column="FCORGCODE", blank=True, null=True)
    FCSELTAG = models.CharField(max_length=1, db_column="FCSELTAG", blank=True, null=True)
    FCSKID = models.CharField(max_length=8, db_column="FCSKID",primary_key=True, editable=False)
    FCSRCUPD = models.CharField(max_length=30, db_column="FCSRCUPD", blank=True, null=True)
    FCU1ACC = models.CharField(max_length=20, db_column="FCU1ACC", blank=True, null=True)
    FCUDATE = models.CharField(max_length=2, db_column="FCUDATE", blank=True, null=True)
    FCUTIME = models.CharField(max_length=2, db_column="FCUTIME", blank=True, null=True)
    FIMILLISEC = models.IntegerField(db_column="FIMILLISEC", blank=True, null=True, default="0")
    FMEXTRATAG = models.TextField(db_column="FMEXTRATAG", blank=True, null=True)
    FNQTY = models.FloatField(db_column="FNQTY", default="0.0", blank=True, null=True)
    FNUMQTY = models.FloatField(db_column="FNUMQTY", default="0.0", blank=True, null=True)
    FTDATETIME= models.DateTimeField(db_column="FTDATETIME", auto_now=True)
    FTLASTEDIT= models.DateTimeField(db_column="FTLASTEDIT", auto_now=True)
    FTLASTUPD= models.DateTimeField(db_column="FTLASTUPD", auto_now=True)
    FTSRCUPD= models.DateTimeField(db_column="FTSRCUPD", auto_now=True)
    
    def __str__(self):
        return self.FCSKID

    class Meta:
        db_table = "NOTECUT"
        app_label = "formular_vcst"