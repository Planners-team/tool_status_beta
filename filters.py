import django_filters
from .models import *

class ToolsFilter(django_filters.FilterSet):
    class Meta:
        model = ts_data
        fields = ['UTID','Tool', 'SO_FID', 'Customer', 'tool_status', 'Open_Date', 'Ship_Date']
 