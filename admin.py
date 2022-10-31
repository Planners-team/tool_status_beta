from django.contrib import admin
from ts_system.models import *
# from import_export.admin import ImportExportModelAdmin


admin.site.register(ts_data)
# class ts_data_Admin(ImportExportModelAdmin):
#     list_display = (ts_data._meta.get_fields())
# # Register your models here.
