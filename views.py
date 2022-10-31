from ast import arg
from cProfile import label
import imp
from itertools import count
from unittest import result
from django.shortcuts import render
from ts_system.models import *
# import requests
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Permission
from django.db.models import Q, F #for the django queries
from django.shortcuts import render, redirect
from ts_system.forms import *
import csv
import datetime
from ts_system.forms import *
from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
import datetime as dt
import pandas as pd
import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_protect
from updateservice import update
from .filters import ToolsFilter
from django.db.models import Q
from django.contrib.auth.models import User, Permission, Group
from django.http import HttpResponse

@login_required
def home(request):
    notification = ''
    if request.GET.get('Reload Data') == 'Reload Data':
        # export_csv_ts_data(request)
        update.get_BP() #first- import updated data from BP
        #now check for each Argo in TS if it exists in BP, if so - update its' fields from BP
        for item in ts_data.objects.exclude(Argo_ID = None):
            argo_ts = item.Argo_ID
            if argo_data.objects.filter(Argo_ID = argo_ts).exists(): 
                tool_argo = argo_data.objects.get(Argo_ID = argo_ts)
                item.BuildQtr = tool_argo.BuildQtr
                item.Customer = tool_argo.fab_name
                item.Ship_Date = tool_argo.commit_date
                item.SO_FID = tool_argo.sales_order
                item.Tool = tool_argo.flex01
                item.Tool_start_date = tool_argo.Tool_start_date
                item.save()
        notification = 'data was reload successfully !'
    family_list = ts_data.objects.order_by().values_list('tool_family', flat=True).distinct()
    context = {
        'family_list' : family_list,
        'searched' : False,
        'notification' : notification,
    }
    if request.method == 'POST':#if 'Search' button was pressed
        search_utid = request.POST.get('search_UTID')
        search_Argo = request.POST.get('search_Argo')
        search_tool = request.POST.get('search_tool')
        search_SO = request.POST.get('search_SO')
        search_customer = request.POST.get('search_customer')
        search_status = request.POST.get('search_status')
        search_wo = request.POST.get('search_wo')
        open_tools = ts_data.objects.filter(IS_SHIPPED = "0")
        if search_utid:
            search_value = search_utid
            results = open_tools.filter(UTID__contains=search_utid)
        elif search_Argo:
            search_value = search_Argo
            results = open_tools.filter(Argo_ID__contains=search_Argo)
        elif search_tool:
            search_value = search_tool
            results = open_tools.filter(Tool__contains=search_tool)
        elif search_SO:
            search_value = search_SO
            results = open_tools.filter(SO_FID__contains=search_SO)
        elif search_customer:
            search_value = search_customer
            results = open_tools.filter(Customer__contains=search_customer)
        elif search_status:
            search_value = search_status
            results = open_tools.filter(tool_status__contains=search_status)
        elif search_wo:
            search_value = search_wo
            results = open_tools.filter(Q(K_MAT__contains=search_wo)|Q(WO1__contains=search_wo)|Q(Tester_Type__contains=search_wo)|Q(WO2__contains=search_wo)|Q(BBSE__contains=search_wo)|Q(WO3__contains=search_wo)|Q(WLR_FD__contains=search_wo)|Q(WO4__contains=search_wo)|Q(OPTION_LDSR__contains=search_wo)|Q(WO5__contains=search_wo)|Q(UVR_eUVR__contains=search_wo)|Q(WO6__contains=search_wo)|Q(AiD_SSiD__contains=search_wo)|Q(WO7__contains=search_wo)|Q(Compensator__contains=search_wo)|Q(WO8__contains=search_wo)|Q(MSWAVECAL__contains=search_wo)|Q(WO9__contains=search_wo)|Q(NLR_Ceramic_Chuck__contains=search_wo)|Q(WO10__contains=search_wo))
            # writer.writerow(['UTID', 'Tool', 'SO_FID', 'Customer', 'tool_status', 'Open_Date', 'Ship_Date', 'Comment', 'Handler', 'K_MAT', 'WO1', 'Tester_Type', 'WO2', 'BBSE', 'WO3', 'WLR_FD', 'WO4', 'OPTION_LDSR', 'WO5', 'UVR_eUVR', 'WO6', 'AiD_SSiD', 'WO7', 'Compensator', 'WO8', 'MSWAVECAL', 'WO9', 'NLR_Ceramic_Chuck', 'WO10', 'Others', 'Comments2', 'IS_SHIPPED'])
        num_results = len(results)
        context = {
            'family_list' : family_list,
            'searched' : True,
            'results' : results,
            'notification' : notification,
            'num_results' : num_results,
            "search_value" : search_value,
        }
        return render(request, 'ts_system/searched.html',context)
    return render(request, 'ts_system/home.html',context)
    
@login_required
def family_page(request):
    # Get family_name from request
    family_name = request.GET.get('tool_family')
    objects = ts_data.objects.filter(tool_family = family_name) #if we don't want to seperate the data into families, just leave: objects = ts_data.objects.all()
    myFilter = ToolsFilter(request.GET, queryset=objects)
    objects = myFilter.qs
    options_list = ["True","False"]
    not_shipped= ts_data.objects.filter(Q(IS_SHIPPED = "0") & Q(tool_family = family_name))#if we don't want to seperate the data into families remove this: & Q(tool_family = family_name)
    num_results = len(not_shipped)
    context = {
        'utids' : not_shipped,
        'form' : is_shipped_Form,
        "myFilter" : myFilter,
        "family_name" : family_name,
        "options_list" : options_list,
        "num_results" : num_results,
    }
    if request.method == 'POST':#if submit button was pressed
        id = request.POST.get('id','') 
        IS_SHIPPED_value = request.POST.get('IS_SHIPPED')
        UTID = ts_data.objects.get(UTID = id)
        UTID.IS_SHIPPED = IS_SHIPPED_value
        UTID.save()
    return render(request, 'ts_system/family_page.html',context)

@login_required
def shipped(request):
    shipped=ts_data.objects.filter(IS_SHIPPED = "1")
    return render(request, 'ts_system/shipped.html',{'utids':shipped})

@login_required
def dashboard(request):
    num_utids = ts_data.objects.count()
    shipped= ts_data.objects.filter(IS_SHIPPED = "1").count()
    not_shipped= ts_data.objects.filter(IS_SHIPPED = "0").count()
    num_types = ts_data.objects.values('Tool').distinct().count()
    empty_wos1 = ts_data.objects.filter((Q(WO1 = "") | Q(WO1 = None)) & Q(IS_SHIPPED = "0")).count()
    empty_wos2 = ts_data.objects.filter((Q(WO2 = "") | Q(WO2 = None)) & Q(IS_SHIPPED = "0")).count()
    empty_wos3 = ts_data.objects.filter((Q(WO3 = "") | Q(WO3 = None)) & Q(IS_SHIPPED = "0")).count()
    empty_wos4 = ts_data.objects.filter((Q(WO4 = "") | Q(WO4 = None)) & Q(IS_SHIPPED = "0")).count()
    empty_wos5 = ts_data.objects.filter((Q(WO5 = "") | Q(WO5 = None)) & Q(IS_SHIPPED = "0")).count()
    empty_wos6 = ts_data.objects.filter((Q(WO6 = "") | Q(WO6 = None)) & Q(IS_SHIPPED = "0")).count()
    empty_wos7 = ts_data.objects.filter((Q(WO7 = "") | Q(WO7 = None)) & Q(IS_SHIPPED = "0")).count()
    empty_wos8 = ts_data.objects.filter((Q(WO8 = "") | Q(WO8 = None)) & Q(IS_SHIPPED = "0")).count()
    empty_wos9 = ts_data.objects.filter((Q(WO9 = "") | Q(WO9 = None)) & Q(IS_SHIPPED = "0")).count()
    empty_wos10 = ts_data.objects.filter((Q(WO10 = "") | Q(WO10 = None)) & Q(IS_SHIPPED = "0")).count()
    total_empty_wos = empty_wos1 + empty_wos2 + empty_wos3 + empty_wos4 + empty_wos5 + empty_wos6 + empty_wos7 +empty_wos8 + empty_wos9 + empty_wos10
    
    open_tools = ts_data.objects.filter(IS_SHIPPED = "0")
    for tool_open in open_tools:
        if argo_data.objects.filter(Argo_ID = tool_open.Argo_ID).exists():
            tool_argo = argo_data.objects.get(Argo_ID = tool_open.Argo_ID)
            tool_open.BuildQtr = tool_argo.BuildQtr
            tool_open.save()
    
    SAP_fields = 'Order'
    ts_fields = 'WO1', 'WO10', 'WO2', 'WO3', 'WO4', 'WO5', 'WO6', 'WO7', 'WO8', 'WO9'
    # SAP_values =  wos.objects.order_by().values_list(SAP_fields, flat=True).distinct()
    # ts_values = ts_data.objects.order_by().values_list(ts_fields, flat=True).distinct()

    # # in_TS_not_SAP = ts_data.objects.exclude(wos__Order="")
    # # in_SAP_not_TS = wos.objects.exclude(ts_data__WO1_WO10_WO2_WO3_WO4_WO5_WO6_WO7_WO8_WO9=1)
    # in_TS_not_SAP = SAP_values - ts_values
    # in_SAP_not_TS = ts_values - SAP_values
    # num_in_TS_not_SAP = in_TS_not_SAP.count()
    # num_in_SAP_not_TS = in_SAP_not_TS.count()

    dictionary_BuildQtr = {}
    for qtr in open_tools.order_by().values_list('BuildQtr', flat=True).distinct():
        key = qtr
        value = open_tools.filter(BuildQtr = qtr).count()
        dictionary_BuildQtr[key] = value
    
    context = {
        "num_utids" : num_utids,
        "shipped" : shipped,
        "not_shipped" : not_shipped,
        "num_types" : num_types,
        "total_empty_wos" : total_empty_wos,
        "keys" : dictionary_BuildQtr.keys(),
        "values" : dictionary_BuildQtr.values(),
        # "in_TS_not_SAP" : in_TS_not_SAP,
        # "in_SAP_not_TS" : in_SAP_not_TS,
        # "num_in_TS_not_SAP" : num_in_TS_not_SAP,
        # "num_in_SAP_not_TS" : num_in_SAP_not_TS,
    }
    return render(request, 'ts_system/dashboard.html',context)

@login_required
def missing_wos(request):
    missing_wos = ts_data.objects.filter(Q(IS_SHIPPED = "0") & (Q(WO1="")|Q(WO1=None)|Q(WO2="")|Q(WO2=None)|Q(WO3="")|Q(WO3=None)|Q(WO4="")|Q(WO4=None)|Q(WO5="")|Q(WO5=None)|Q(WO6="")|Q(WO6=None)|Q(WO7="")|Q(WO7=None)|Q(WO8="")|Q(WO8=None)|Q(WO9="")|Q(WO9=None)|Q(WO10="")|Q(WO10=None)))
    context = {
        'utids' : missing_wos,
    }
    return render(request, 'ts_system/missing_wos.html',context)

@login_required
def in_TS_not_SAP(request):
    in_TS_not_SAP = ts_data.objects.exclude(wos_id=1)
    context = {
        'utids' : in_TS_not_SAP,
    }
    return render(request, 'ts_system/in_TS_not_SAP.html',context)

@login_required
def in_SAP_not_TS(request):
    in_SAP_not_TS = wos.objects.exclude(ts_data_id=1)
    context = {
        'utids' : in_SAP_not_TS,
    }
    return render(request, 'ts_system/in_SAP_not_TS.html',context)

@login_required
def new_UTID(request):
    results = ts_data.objects.all()
    family_list = ts_data.objects.order_by().values_list('tool_family', flat=True).distinct()
    alert = ''
    context = {
        "message" : alert,
        "results" : results,
        "family_list" : family_list,
        }
    if request.method == 'POST':#if submit button was pressed
        Argo_ID = request.POST.get('Argo_ID')
        Configuration_path = update.FindFiles(Argo_ID)
        UTID = request.POST.get('UTID')
        #Check if UTID already exists in TS:
        if ts_data.objects.filter(UTID = UTID).exists():
                alert = 'ERROR! UTID is already exists'
                context = {
                "message" : alert,
                "results" : results,
                "family_list" : family_list,
                }
        #Check if Argo ID already exists in TS:
        elif ts_data.objects.filter(Argo_ID = Argo_ID).exists():
            alert = 'ERROR! Argo ID is already exists'
            context = {
            "message" : alert,
            "results" : results,
            "family_list" : family_list,
            }
        #check if Argo exists in BP:
        else: #first pull data from Argo and then check if Argo exists in BP
            update.get_BP()
            if argo_data.objects.filter(Argo_ID = Argo_ID).exists(): 
                #if it does, create the UTID and import fields from BP
                # # update.get_data_for_new_Argo(UTID, Argo_ID)
                argo_entity = argo_data.objects.get(Argo_ID = Argo_ID)
                alert = "UTID created successfully"
                context = {
                "message" : alert,
                "results" : results,
                "family_list" : family_list,
                }
                Argo_ID = request.POST.get('Argo_ID') # Argo_ID entered by user
                UTID = request.POST.get('UTID') # UTID entered by user
                argo_entity = argo_data.objects.get(Argo_ID = Argo_ID)
                argo_Tool = argo_entity.flex01
                argo_SO_FID = argo_entity.sales_order
                argo_Customer = argo_entity.fab_name
                argo_Ship_Date = argo_entity.commit_date
                current_date = datetime.datetime.now()  
                new_entity = ts_data(Argo_ID = request.POST.get('Argo_ID'),
                                    tool_family = request.POST.get('tool_family'),
                                    tool_status = request.POST.get('tool_status'),
                                    UTID = UTID,
                                    Tool = argo_Tool,
                                    SO_FID = argo_SO_FID,
                                    Customer = argo_Customer,
                                    Ship_Date = argo_Ship_Date,
                                    Open_Date = current_date,
                                    Configuration = Configuration_path
                                    )
                new_entity.save()  
            else: #argo does not exist in BP
                Argo_ID = request.POST.get('Argo_ID') # Argo_ID entered by user
                UTID = request.POST.get('UTID') # UTID entered by user
                current_date = datetime.datetime.now()  
                new_entity = ts_data(Argo_ID = request.POST.get('Argo_ID'),
                                    tool_family = request.POST.get('tool_family'),
                                    tool_status = request.POST.get('tool_status'),
                                    Open_Date = current_date,
                                    UTID = UTID,
                                    )
                new_entity.save()  
                alert = "UTID created successfully but please notice(!) the Argo ID does not exist in BP"
                context = {
                    "message" : alert,
                    "results" : results,
                    "family_list" : family_list,
                    }
    return render(request, 'ts_system/new_UTID.html', context)

@login_required
def transfer_shipped_to_open(request):
    results = ts_data.objects.all()
    message = ''
    context = {
        "message" : message,
        "results" : results,
        }
    if request.method == "POST":#if submit button was pressed
        message = 'UTID is now an Open Tool'
        context = {
            "message" : message,
            "results" : results,
            }
        UTID_to_transfer = request.POST.get('utid_transfer')
        first_entity = ts_data.objects.get(UTID = UTID_to_transfer)
        first_entity.IS_SHIPPED = False
        first_entity.save()
    return render(request, 'ts_system/transfer_shipped_to_open.html', context)

@login_required
def swap_UTIDs(request):
    results = ts_data.objects.all()
    message = ''
    context = {
        "message" : message,
        "results" : results,
        }
    if request.method == "POST":#if submit button was pressed
        message = 'UTIDs swaped successfully'
        context = {
            "message" : message,
            "results" : results,
            }
        First_UTID = request.POST.get('first')
        Second_UTID = request.POST.get('second')
        first_entity = ts_data.objects.get(UTID = First_UTID)
        second_entity = ts_data.objects.get(UTID = Second_UTID)

    #save all fields of the first UTID into temp fileds: 
        tool_family = first_entity.tool_family        
        Tool = first_entity.Tool
        SO_FID = first_entity.SO_FID
        Customer = first_entity.Customer
        tool_status = first_entity.tool_status
        Open_Date = first_entity.Open_Date
        Ship_Date = first_entity.Ship_Date
        Comment = first_entity.Comment
        Handler = first_entity.Handler
        K_MAT = first_entity.K_MAT
        WO1 = first_entity.WO1
        Tester_Type = first_entity.Tester_Type
        WO2 = first_entity.WO2
        BBSE = first_entity.BBSE
        WO3 = first_entity.WO3
        WLR_FD = first_entity.WLR_FD
        WO4 = first_entity.WO4
        OPTION_LDSR = first_entity.OPTION_LDSR
        WO5 = first_entity.WO5
        UVR_eUVR = first_entity.UVR_eUVR
        WO6 = first_entity.WO6
        AiD_SSiD = first_entity.AiD_SSiD
        WO7 = first_entity.WO7
        Compensator = first_entity.Compensator
        WO9 = first_entity.WO9
        NLR_Ceramic_Chuck = first_entity.NLR_Ceramic_Chuck
        WO10 = first_entity.WO10
        Others = first_entity.Others
        Comments2 = first_entity.Comments2
        IS_SHIPPED = first_entity.IS_SHIPPED
        BuildQtr = first_entity.BuildQtr
        Voucher = first_entity.Voucher
        Tool_start_date = first_entity.Tool_start_date
        Configuration = first_entity.Configuration
        Argo_ID = first_entity.Argo_ID
        Tool_owner = first_entity.Tool_owner

    #replace all fields of the first UTID with the fields of the second UTID:                
        first_entity.tool_family = second_entity.tool_family        
        first_entity.Tool = second_entity.Tool
        first_entity.SO_FID = second_entity.SO_FID
        first_entity.Customer = second_entity.Customer
        first_entity.tool_status = second_entity.tool_status
        first_entity.Open_Date = second_entity.Open_Date
        first_entity.Ship_Date = second_entity.Ship_Date
        first_entity.Comment = second_entity.Comment
        first_entity.Handler = second_entity.Handler
        first_entity.K_MAT = second_entity.K_MAT
        first_entity.WO1 = second_entity.WO1
        first_entity.Tester_Type = second_entity.Tester_Type
        first_entity.WO2 = second_entity.WO2
        first_entity.BBSE = second_entity.BBSE
        first_entity.WO3 = second_entity.WO3
        first_entity.WLR_FD = second_entity.WLR_FD
        first_entity.WO4 = second_entity.WO4
        first_entity.OPTION_LDSR = second_entity.OPTION_LDSR
        first_entity.WO5 = second_entity.WO5
        first_entity.UVR_eUVR = second_entity.UVR_eUVR
        first_entity.WO6 = second_entity.WO6
        first_entity.AiD_SSiD = second_entity.AiD_SSiD
        first_entity.WO7 = second_entity.WO7
        first_entity.Compensator = second_entity.Compensator
        first_entity.WO9 = second_entity.WO9
        first_entity.NLR_Ceramic_Chuck = second_entity.NLR_Ceramic_Chuck
        first_entity.WO10 = second_entity.WO10
        first_entity.Others = second_entity.Others
        first_entity.Comments2 = second_entity.Comments2
        first_entity.IS_SHIPPED = second_entity.IS_SHIPPED
        first_entity.Voucher = second_entity.Voucher
        first_entity.Tool_start_date = second_entity.Tool_start_date
        first_entity.Configuration = second_entity.Configuration
        first_entity.BuildQtr = second_entity.BuildQtr
        first_entity.Argo_ID = second_entity.Argo_ID
        first_entity.Tool_owner = second_entity.Tool_owner
        first_entity.save() #save the First UTID with it's new fields

    #replace all fields of the second UTID with the fields of the first UTID by using the temp fields we saved earlier:                
        second_entity.tool_family = tool_family        
        second_entity.Tool = Tool
        second_entity.SO_FID = SO_FID
        second_entity.Customer = Customer
        second_entity.tool_status = tool_status
        second_entity.Open_Date = Open_Date
        second_entity.Ship_Date = Ship_Date
        second_entity.Comment = Comment
        second_entity.Handler = Handler
        second_entity.K_MAT = K_MAT
        second_entity.WO1 = WO1
        second_entity.Tester_Type = Tester_Type
        second_entity.WO2 = WO2
        second_entity.BBSE = BBSE
        second_entity.WO3 = WO3
        second_entity.WLR_FD = WLR_FD
        second_entity.WO4 = WO4
        second_entity.OPTION_LDSR = OPTION_LDSR
        second_entity.WO5 = WO5
        second_entity.UVR_eUVR = UVR_eUVR
        second_entity.WO6 = WO6
        second_entity.AiD_SSiD = AiD_SSiD
        second_entity.WO7 = WO7
        second_entity.Compensator = Compensator
        second_entity.WO9 = WO9
        second_entity.NLR_Ceramic_Chuck = NLR_Ceramic_Chuck
        second_entity.WO10 = WO10
        second_entity.Others = Others
        second_entity.Comments2 = Comments2
        second_entity.IS_SHIPPED = IS_SHIPPED
        second_entity.Voucher = Voucher
        second_entity.Tool_start_date = Tool_start_date
        second_entity.Configuration = Configuration
        second_entity.BuildQtr = BuildQtr
        second_entity.Argo_ID = Argo_ID
        second_entity.Tool_owner = Tool_owner
        second_entity.save() #save the second UTID with it's new fields
    return render(request, 'ts_system/swap_UTIDs.html', context)

@login_required
def delete_UTID(request):
    results = ts_data.objects.order_by('UTID').all()
    message = ''
    context = {
        "message" : message,
        "results" : results,
        }
    if request.method == "POST":#if submit button was pressed
        message = "UTID was removed from DB successfully"
        context = {
            "message" : message,
            "results" : results,
            }
        remove_utid = request.POST.get('remove_utid')
        to_remove = ts_data.objects.ContactFormget(UTID = remove_utid)
        to_remove.delete()
    return render(request, 'ts_system/delete_UTID.html',context)

@login_required
def find_UTIDs(request):
    form = Find_UTID_Form
    if request.method == 'POST':
        form = Find_UTID_Form(request.POST)
        if form.is_valid():
            UTIDs = form.cleaned_data.get('UTIDs')
            context = {
                "form" : form,
                }
            return render(request, 'ts_system/searched.html',context)
    else:
        form = Find_UTID_Form
    return render(request, 'ts_system/find_UTIDs.html',{"form":form})


@login_required
def compare(request):
    all_data = ts_data.objects.all()
    context = {
        "objects" : all_data
    }
    return render(request, 'ts_system/compare.html')

@login_required
def export_csv_ts_data(request):
    response =HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename= Tool_Status ' + str(datetime.datetime.now()) + '.csv'
    writer = csv.writer(response)
    writer.writerow(['UTID', 'Argo ID', 'Tool', 'SO_FID', 'Customer', 'tool_status', 'Open_Date', 'Ship_Date', 'Comment', 'Handler', 'K_MAT', 'WO1', 'Tester_Type', 'WO2', 'BBSE', 'WO3', 'WLR_FD', 'WO4', 'OPTION_LDSR', 'WO5', 'UVR_eUVR', 'WO6', 'AiD_SSiD', 'WO7', 'Compensator', 'WO8', 'MSWAVECAL', 'WO9', 'NLR_Ceramic_Chuck', 'WO10', 'Others', 'Comments2', 'IS_SHIPPED', 'Voucher', 'Tool_start_date', 'Configuration'])
    ts_system = ts_data.objects.all()
    for item in ts_system:
        writer.writerow([item.UTID, item.Argo_ID, item.Tool, item.SO_FID, item.Customer, item.tool_status, item.Open_Date, item.Ship_Date, item.Comment, item.Handler, item.K_MAT, item.WO1, item.Tester_Type, item.WO2, item.BBSE, item.WO3, item.WLR_FD, item.WO4, item.OPTION_LDSR, item.WO5, item.UVR_eUVR, item.WO6, item.AiD_SSiD, item.WO7, item.Compensator, item.WO8, item.MSWAVECAL, item.WO9, item.NLR_Ceramic_Chuck, item.WO10, item.Others, item.Comments2, item.IS_SHIPPED, item.Voucher, item.Tool_start_date, item.Configuration])
    return response

@login_required
def export_csv_shipped_only(request):
    response =HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename= Shipped_Tools ' + str(datetime.datetime.now()) + '.csv'
    writer = csv.writer(response)
    writer.writerow(['UTID', 'Argo ID', 'Tool', 'SO_FID', 'Customer', 'tool_status', 'Open_Date', 'Ship_Date', 'Comment', 'Handler', 'K_MAT', 'WO1', 'Tester_Type', 'WO2', 'BBSE', 'WO3', 'WLR_FD', 'WO4', 'OPTION_LDSR', 'WO5', 'UVR_eUVR', 'WO6', 'AiD_SSiD', 'WO7', 'Compensator', 'WO8', 'MSWAVECAL', 'WO9', 'NLR_Ceramic_Chuck', 'WO10', 'Others', 'Comments2', 'IS_SHIPPED', 'Voucher', 'Tool_start_date', 'Configuration'])
    ts_system = ts_data.objects.filter(IS_SHIPPED = "1")
    for item in ts_system:
        writer.writerow([item.UTID, item.Argo_ID, item.Tool, item.SO_FID, item.Customer, item.tool_status, item.Open_Date, item.Ship_Date, item.Comment, item.Handler, item.K_MAT, item.WO1, item.Tester_Type, item.WO2, item.BBSE, item.WO3, item.WLR_FD, item.WO4, item.OPTION_LDSR, item.WO5, item.UVR_eUVR, item.WO6, item.AiD_SSiD, item.WO7, item.Compensator, item.WO8, item.MSWAVECAL, item.WO9, item.NLR_Ceramic_Chuck, item.WO10, item.Others, item.Comments2, item.IS_SHIPPED, item.Voucher, item.Tool_start_date, item.Configuration])
    return response

@login_required
def export_csv_not_shipped(request):
    response =HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename= Tool_Status ' + str(datetime.datetime.now()) + '.csv'
    writer = csv.writer(response)
    writer.writerow(['UTID', 'Argo ID', 'Tool', 'SO_FID', 'Customer', 'tool_status', 'Open_Date', 'Ship_Date', 'Comment', 'Handler', 'K_MAT', 'WO1', 'Tester_Type', 'WO2', 'BBSE', 'WO3', 'WLR_FD', 'WO4', 'OPTION_LDSR', 'WO5', 'UVR_eUVR', 'WO6', 'AiD_SSiD', 'WO7', 'Compensator', 'WO8', 'MSWAVECAL', 'WO9', 'NLR_Ceramic_Chuck', 'WO10', 'Others', 'Comments2', 'IS_SHIPPED', 'Voucher', 'Tool_start_date', 'Configuration'])
    ts_system = ts_data.objects.filter(IS_SHIPPED = "0")
    for item in ts_system:
        writer.writerow([item.UTID, item.Argo_ID, item.Tool, item.SO_FID, item.Customer, item.tool_status, item.Open_Date, item.Ship_Date, item.Comment, item.Handler, item.K_MAT, item.WO1, item.Tester_Type, item.WO2, item.BBSE, item.WO3, item.WLR_FD, item.WO4, item.OPTION_LDSR, item.WO5, item.UVR_eUVR, item.WO6, item.AiD_SSiD, item.WO7, item.Compensator, item.WO8, item.MSWAVECAL, item.WO9, item.NLR_Ceramic_Chuck, item.WO10, item.Others, item.Comments2, item.IS_SHIPPED, item.Voucher, item.Tool_start_date, item.Configuration])
    return response

@login_required
def export_csv_sap_data(request):
    response =HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename= ARGO DATA ' + str(datetime.datetime.now()) + '.csv'
    writer = csv.writer(response)
    writer.writerow(['Argo ID', 'UTID', 'flex01', 'sales order', 'fab name', 'commit date', 'Build Qtr'])
    sap_items = argo_data.objects.all()
    for item in sap_items:
        writer.writerow([item.Argo_ID, item.Argo_ID, item.UTID, item.flex01, item.sales_order, item.fab_name, item.commit_date, item.BuildQtr,item.Tool_start_date])
    return response
      
@login_required
def argo_page(request):
    notification = ''
    data = argo_data.objects.all()
    context = {
            'utids' : data,
            'notification' : notification
        }
    # if request.GET.get('Refresh') == 'Refresh':
    #     update.get_BP()
    #     data = argo_data.objects.all()
    #     #now check for each Argo in TS if it exists in BP, if so - update its' fields from BP
    #     for item in ts_data.objects.exclude(Argo_ID = None).exclude(Argo_ID = ''):
    #         argo_ts = item.Argo_ID
    #         if argo_data.objects.filter(Argo_ID = argo_ts).exists(): 
    #             tool_argo = argo_data.objects.get(Argo_ID = argo_ts)
    #             item.BuildQtr = tool_argo.BuildQtr
    #             item.fab_name = tool_argo.fab_name
    #             item.commit_date = tool_argo.commit_date
    #             item.sales_order = tool_argo.sales_order
    #             item.flex01 = tool_argo.flex01
    #             item.Tool_start_date = tool_argo.Tool_start_date
    #             item.save()
    #     notification = 'data was reload successfully !'
    context = {
        'utids' : data,
        'notification' : notification
        }
    return render(request, 'ts_system/argo_page.html',context)

@login_required
def daily_page(request):
    notification = ''
    data = daily_data.objects.all()
    context = {
            'utids' : data,
            'notification' : notification
        }
    if request.method == 'POST':#if submit button was pressed
        data = update.get_daily()
        notification = 'data was refreshed successfully !'
        context = {
            'utids' : data,
            'notification' : notification
        }
    return render(request, 'ts_system/daily_page.html',context)

@login_required
def shipped(request):
    shipped=ts_data.objects.filter(IS_SHIPPED = "1")
    return render(request, 'ts_system/shipped.html',{'utids':shipped})

@login_required
def saveUTID(request):
    id = request.POST.get('id','')    
    type = request.POST.get('type','')
    value = request.POST.get('value','')
    IS_SHIPPED_value = request.POST.get('IS_SHIPPED'),
    UTID = ts_data.objects.get(UTID = id)
    if type == 'Tool':
        UTID.Tool = value
    if type == 'SO_FID':
        UTID.SO_FID = value
    if type == 'Customer':
        UTID.Customer = value
    if type == 'tool_status':
        UTID.tool_status = value
    if type == 'Open_Date':
        UTID.Open_Date = value
    if type == 'Ship_Date':
        UTID.Ship_Date = value
    if type == 'Comment':
        UTID.Comment = value
    if type == 'Handler':
        UTID.Handler = value
    if type == 'K_MAT':
        UTID.K_MAT = value
    if type == 'WO1':
        UTID.WO1 = value
    if type == 'Tester_Type':
        UTID.Tester_Type = value
    if type == 'WO2':
        UTID.WO2 = value
    if type == 'BBSE':
        UTID.BBSE = value
    if type == 'WO3':
        UTID.WO3 = value
    if type == 'WLR_FD':
        UTID.WLR_FD = value
    if type == 'WO4':
        UTID.WO4 = value
    if type == 'OPTION_LDSR':
        UTID.OPTION_LDSR = value
    if type == 'WO5':
        UTID.WO5 = value
    if type == 'UVR_eUVR':
        UTID.UVR_eUVR = value
    if type == 'WO6':
        UTID.WO6 = value
    if type == 'AiD_SSiD':
        UTID.AiD_SSiD = value
    if type == 'WO7':
        UTID.WO7 = value   
    if type == 'Compensator':
        UTID.Compensator = value
    if type == 'WO8':
        UTID.WO8 = value
    if type == 'MSWAVECAL':
        UTID.MSWAVECAL = value
    if type == 'WO9':
        UTID.WO9 = value
    if type == 'NLR_Ceramic_Chuck':
        UTID.NLR_Ceramic_Chuck = value
    if type == 'WO10':
        UTID.WO10 = value
    if type == 'Others':
        UTID.Others = value
    if type == 'Comments2':
        UTID.Comments2 = value
    if type == 'tool_family':
        UTID.tool_family = value 
    if type == 'Voucher':
        UTID.Voucher = value 
    if type == 'IS_SHIPPED':
        UTID.IS_SHIPPED = value     
    # UTID.IS_SHIPPED = IS_SHIPPED_value

    UTID.save()
    return JsonResponse({"seccess":"Updated"})

# @csrf_protect
@login_required
def update_utid(request,utid_id):
    UTID = ts_data.objects.get(UTID=utid_id)
    if UTID == None:
        return HttpResponse("UTID Not Found")
    else:
        UTID.Tool=request.POST.get('Tool','')
        UTID.SO_FID=request.POST.get('SO_FID','')
        UTID.Customer=request.POST.get('Customer','')
        UTID.tool_status=request.POST.get('tool_status','')
        UTID.Open_Date=request.POST.get('Open_Date','')
        UTID.Ship_Date=request.POST.get('Ship_Date','')
        UTID.Comment=request.POST.get('Comment','')
        UTID.Handler=request.POST.get('Handler','')
        UTID.K_MAT=request.POST.get('K_MAT','')
        UTID.WO1=request.POST.get('WO1','')
        UTID.Tester_Type=request.POST.get('Tester_Type','')
        UTID.WO2=request.POST.get('WO2','')
        UTID.BBSE=request.POST.get('BBSE','')
        UTID.WO3=request.POST.get('WO3','')
        UTID.WLR_FD=request.POST.get('WLR_FD','')
        UTID.WO4=request.POST.get('WO4','')
        UTID.OPTION_LDSR=request.POST.get('OPTION_LDSR','')
        UTID.WO5=request.POST.get('WO5','')
        UTID.UVR_eUVR=request.POST.get('UVR_eUVR','')
        UTID.WO6=request.POST.get('WO6','')
        UTID.AiD_SSiD=request.POST.get('AiD_SSiD','')
        UTID.WO7=request.POST.get('WO7','')
        UTID.Compensator=request.POST.get('Compensator','')
        UTID.WO8=request.POST.get('WO8','')
        UTID.MSWAVECAL=request.POST.get('MSWAVECAL','')
        UTID.WO9=request.POST.get('WO9','')
        UTID.NLR_Ceramic_Chuck=request.POST.get('NLR_Ceramic_Chuck','')
        UTID.WO10=request.POST.get('WO10','')
        UTID.Others=request.POST.get('Others','')
        UTID.Comments2=request.POST.get('Comments2','')
        UTID.IS_SHIPPED=request.POST.get('IS_SHIPPED','')
        UTID.Voucher=request.POST.get('Voucher','')
        UTID.Tool_start_date=request.POST.get('Tool_start_date','')
        UTID.Configuration=request.POST.get('Configuration','')
        UTID.save()
    return render(request, 'ts_system/home.html')

@login_required
def all_users(request):
    users = User.objects.all()
    return render(request, 'ts_system/all_users.html',{'users':users})

@login_required
def new_user(request):
    message = ''
    l_groups = Group.objects.values_list('name',flat = True) # QuerySet Object
    groups = list(l_groups)                                     # QuerySet to `list`
    # groups = Group.objects.order_by().values_list().distinct()
    if request.method == 'POST':#if submit button was pressed
        user_name = request.POST.get('user_name')
        email = request.POST.get('email') 
        password = request.POST.get('password') 
        permissions = request.POST.get('permissions')
        new_user = User.objects.create_user(username= user_name,
                                 email= email,
                                 password= password)
        message = 'User was created successfuly'
        g = Group.objects.get(name=permissions)
        g.user_set.add(new_user)
    context = {
            'message' : message,
            'groups' : groups,
        }
    return render(request, 'ts_system/new_user.html', context)

@login_required
def edit_user(request):
    message = ''
    users = User.objects.all()
    l_groups = Group.objects.values_list('name',flat = True) # QuerySet Object
    groups = list(l_groups)
    if request.method == 'POST':#if submit button was pressed
        user_name = request.POST.get('user_name')
        permissions = request.POST.get('permissions')
        user = User.objects.get(username= user_name)
        g = Group.objects.get(name=permissions)
        user.groups.clear()
        g.user_set.add(user)
        message = 'User permisions was updated successfuly'
    context = {
            'message' : message,
            'users' : users,
            'groups' : groups,
        }
    return render(request, 'ts_system/edit_user.html',context)
