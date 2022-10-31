# from winreg import KEY_ENUMERATE_SUB_KEYS
from django.db import models
from django.forms import ModelForm, Textarea
from django.db import models                              

class ts_data(models.Model):
    UTID = models.CharField(max_length=250, primary_key=True, unique=True, blank=False)
    Argo_ID = models.CharField(max_length=250, blank=True, null=True)
    Tool = models.CharField(max_length=250, blank=True, null=True)
    SO_FID = models.CharField(max_length=250, blank=True, null=True)
    Customer = models.CharField(max_length=100000, blank=True, null=True)
    tool_status = models.CharField(max_length=250, blank=True, null=True)
    Open_Date = models.CharField(max_length=250, blank=True, null=True) 
    Ship_Date  = models.CharField(max_length=250, blank=True, null=True)
    Comment = models.CharField(max_length=250, blank=True, null=True)
    Handler = models.CharField(max_length=250, blank=True, null=True) 
    K_MAT = models.CharField(max_length=250, blank=True, null=True)
    WO1 = models.CharField(max_length=250, blank=True, null=True)
    Tester_Type = models.CharField(max_length=250, blank=True, null=True)
    WO2 = models.CharField(max_length=250, blank=True, null=True)
    BBSE = models.CharField(max_length=250, blank=True, null=True)
    WO3 = models.CharField(max_length=250, blank=True, null=True)
    WLR_FD = models.CharField(max_length=250, blank=True, null=True)
    WO4 = models.CharField(max_length=250, blank=True, null=True)
    OPTION_LDSR = models.CharField(max_length=250, blank=True, null=True)
    WO5 = models.CharField(max_length=250, blank=True, null=True)
    UVR_eUVR = models.CharField(max_length=250, blank=True, null=True)
    WO6 = models.CharField(max_length=250, blank=True, null=True)
    AiD_SSiD = models.CharField(max_length=250, blank=True, null=True)
    WO7 = models.CharField(max_length=250, blank=True, null=True)
    Compensator = models.CharField(max_length=250, blank=True, null=True)
    WO8 = models.CharField(max_length=250, blank=True, null=True)
    MSWAVECAL = models.CharField(max_length=250, blank=True, null=True)
    WO9 = models.CharField(max_length=250, blank=True, null=True)
    NLR_Ceramic_Chuck = models.CharField(max_length=250, blank=True, null=True)
    WO10 = models.CharField(max_length=250, blank=True, null=True)
    Others = models.CharField(max_length=250, blank=True, null=True)
    Comments2 = models.CharField(max_length=250, blank=True, null=True)
    Tool_owner = models.CharField(max_length=250, blank=True, null=True)
    IS_SHIPPED = models.BooleanField(default=False)
    tool_family = models.CharField(max_length=250, blank=True, null=True)
    BuildQtr = models.CharField(max_length=250, blank=True, null=True)
    Configuration = models.CharField(max_length=250, blank=True, null=True)
    Tool_start_date = models.CharField(max_length=250, blank=True, null=True)
    Voucher = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
        return self.UTID

class argo_data(models.Model):
    Argo_ID = models.CharField(max_length=250, default=None)
    UTID = models.CharField(max_length=250, blank=True, null=True)
    flex01 = models.CharField(max_length=250, blank=True, null=True)
    sales_order = models.CharField(max_length=250, blank=True, null=True)
    fab_name = models.CharField(max_length=250, blank=True, null=True)
    commit_date = models.CharField(max_length=250, blank=True, null=True)
    BuildQtr = models.CharField(max_length=250, blank=True, null=True)
    Tool_start_date = models.DateField(blank=True, null=True)

class previous_argo_data(models.Model):
    Argo_ID = models.CharField(max_length=250, default=None)
    UTID = models.CharField(max_length=250, blank=True, null=True)
    flex01 = models.CharField(max_length=250, blank=True, null=True)
    sales_order = models.CharField(max_length=250, blank=True, null=True)
    fab_name = models.CharField(max_length=250, blank=True, null=True)
    commit_date = models.CharField(max_length=250, blank=True, null=True)
    BuildQtr = models.CharField(max_length=250, blank=True, null=True)
    Tool_start_date = models.DateField(blank=True, null=True)

class daily_data(models.Model):
    Argo_ID = models.CharField(max_length=250, primary_key=True, unique=True,blank=False, null=False)
    UTID = models.CharField(max_length=250, blank=True, null=True)
    flex01 = models.CharField(max_length=250, blank=True, null=True)
    sales_order = models.CharField(max_length=250, blank=True, null=True)
    fab_name = models.CharField(max_length=250, blank=True, null=True)
    commit_date = models.CharField(max_length=250, blank=True, null=True)
    BuildQtr = models.CharField(max_length=250, blank=True, null=True)

class Configuration(models.Model):
    Argo_ID = models.CharField(max_length=250, primary_key=True, unique=True,blank=False, null=False)
    PNs = models.CharField(max_length=250, blank=True, null=True)

class wos(models.Model):
    Order =  models.CharField(max_length=250, primary_key=True, unique=True,blank=False, null=False)
    Material = models.CharField(max_length=250, blank=True, null=True)
    Material_Description = models.CharField(max_length=250, blank=True, null=True)
    Plant = models.CharField(max_length=250, blank=True, null=True)