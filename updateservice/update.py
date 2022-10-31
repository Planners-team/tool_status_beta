from ast import arg
import subprocess, sys
from django.shortcuts import render
from ts_system.models import *
import requests
from urllib.parse import urlparse
import pandas as pd
import snowflake.connector as sf
from snowflake.sqlalchemy import URL
from sqlalchemy import create_engine
from django.shortcuts import redirect
# from pyexcel_xls import get_data as xls_get
# from pyexcel_xlsx import get_data as xlsx_get
from django.utils.datastructures import MultiValueDictKeyError

#This function imports data from SF only for the new Argo ID the user inserted:
def get_data_for_new_Argo(user_UTID, user_Argo):
    # Delete all records from SAP, before pulling an updated DB:
    argo_data.objects.all().delete()
    #create connection variable - use your own creds
    conn = sf.connect(user='yarden.elgali@kla-tencor.com',
                                    account='klaprod.west-us-2.azure',
                                    warehouse='SS_WH',
                                    database='GEAR',
                                    schema='INSIGHTS',
                                    authenticator="externalbrowser",
                                    autocommit=True)
    # execute_query(connection, query):
    cur = conn.cursor()
    sql = cur.execute(""" SELECT "Plant", "Slot/Argo ID", "Build Qtr", "Fab Name", "Mfg Commit Date", "Sales Document", "Flex 01", "Slot UTID", "Tool Start Date New"  FROM GEAR.INSIGHTS.SLS_ARGO_SLOTPLAN_EXPORT_ALL_LIVE WHERE "Plant"= '4002' """)
    records = sql.fetchall()
    for row in records:
        new_record = argo_data.objects.create(Argo_ID = row[1], BuildQtr = row[2], fab_name = row[3], commit_date = row[4], sales_order = row[5], flex01 = row[6], UTID = row[7], Tool_start_date = row[8])
        new_record.save()      
    return ()
    
#This function imports all data from SF, stores it in argo_data database 
# and matches fields from argo_data to ts_data for each Argo ID which exists in both:
def get_BP():
    # Delete all records from SAP, before pulling an updated DB:
    argo_data.objects.all().delete()
    #create connection variable - use your own creds
    conn = sf.connect(user='yarden.elgali@kla-tencor.com',
                                    account='klaprod.west-us-2.azure',
                                    warehouse='SS_WH',
                                    database='GEAR',
                                    schema='INSIGHTS',
                                    authenticator="externalbrowser",
                                    autocommit=True)
    # execute_query(connection, query):
    cur = conn.cursor()
    sql = cur.execute(""" SELECT "Plant", "Slot/Argo ID", "Build Qtr", "Fab Name", "Mfg Commit Date", "Sales Document", "Flex 01", "Slot UTID", "Tool Start Date New"  FROM GEAR.INSIGHTS.SLS_ARGO_SLOTPLAN_EXPORT_ALL_LIVE WHERE "Plant"= '4002' """)
    # df = sql.fetch_pandas_all()
    # iterate over DataFrame and create your objects
    records = sql.fetchall()
    for row in records:
        new_record = argo_data.objects.create(Argo_ID = row[1], BuildQtr = row[2], fab_name = row[3], commit_date = row[4], sales_order = row[5], flex01 = row[6], UTID = row[7], Tool_start_date = row[8])
        new_record.save()    
    return (argo_data.objects.all())

import os,pandas as pd
def FindFiles(Argo_input):
 Conf_PATH='\\\\klasj\ktfiles\Regions\Israel\Ops\KTI-Material-Group\Master_Planning_Group\Configuration\Fast configurators\Aleris configurators'
 ListArgo=[]
 ListPath=[]
 ListIsShipped=[]
 for root, directories, files in os.walk(Conf_PATH, topdown=False):
  folder_name=str(os.path.basename(root))

  for path in files:
    filename, file_extension = os.path.splitext(path)
    filename=filename.strip()
    if ((file_extension == ".xlsm") or  (file_extension == ".xlsx") )& (filename[:12]=="Configurator"):
     filename=filename.removesuffix('(2)') 
     filename=filename.removesuffix('(1)')
     ListArgo.append(filename[-5:])
     ListPath.append(os.path.join(root, path))
     if "Shipped tools" in str(root):
        ListIsShipped.append("Yes")
     else:
        ListIsShipped.append("")  
 DF_FILES = pd.DataFrame(
  {'Argo_ID': ListArgo,
  'Path': ListPath,
  'IsShipped': ListIsShipped
     })    
 df = DF_FILES.loc[DF_FILES['Argo_ID'] == str(Argo_input)]
 return df.Path.values.tolist()