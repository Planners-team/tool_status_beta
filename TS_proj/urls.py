"""TS_proj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from ts_system import views as ts_system_views
from django.contrib.auth import views as auth_views
from updateservice import update

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',auth_views.LoginView.as_view(), name="login"),
    path('dashboard/',ts_system_views.dashboard, name="dashboard"),
    path('login/',auth_views.LoginView.as_view(), name="login"),
    path('home/',ts_system_views.home, name="home"),
    path('compare/',ts_system_views.compare, name="compare"),
    path('delete_UTID/',ts_system_views.delete_UTID, name="delete_UTID"),
    path('new_UTID/',ts_system_views.new_UTID, name="new_UTID"),
    path('saveUTID/',ts_system_views.saveUTID, name="saveUTID"),
    path('argo_page/',ts_system_views.argo_page, name="argo_page"),
    path('daily_page/',ts_system_views.daily_page, name="daily_page"),
    path('update_utid/<str:utid_id>', ts_system_views.update_utid ,name="update_utid"),
    path('swap_UTIDs/',ts_system_views.swap_UTIDs, name="swap_UTIDs"),
    path('family_page/',ts_system_views.family_page, name="family_page"),
    path('in_SAP_not_TS/',ts_system_views.in_SAP_not_TS, name="in_SAP_not_TS"),
    path('in_TS_not_SAP/',ts_system_views.in_TS_not_SAP, name="in_TS_not_SAP"),
    path('all_users/',ts_system_views.all_users, name="all_users"),
    path('new_user/',ts_system_views.new_user, name="new_user"),
    path('edit_user/',ts_system_views.edit_user, name="edit_user"),
    path('missing_wos/',ts_system_views.missing_wos, name="missing_wos"),
    path('transfer_shipped_to_open/',ts_system_views.transfer_shipped_to_open, name="transfer_shipped_to_open"),
    path('searched/',ts_system_views.home, name="searched"),
    path('shipped/',ts_system_views.shipped, name="shipped"),
    path('find_UTIDs/',ts_system_views.find_UTIDs, name="find_UTIDs"),
    path('export_csv_shipped_only',ts_system_views.export_csv_shipped_only, name="export_csv_shipped_only"),
    path('export_csv_not_shipped',ts_system_views.export_csv_not_shipped, name="export_csv_not_shipped"),
    path('export_csv_sap_data',ts_system_views.export_csv_sap_data, name="export_csv_sap_data"),
    path('export_csv_ts_data',ts_system_views.export_csv_ts_data, name="export_csv_ts_data"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include ('ts_system.urls'))
]
