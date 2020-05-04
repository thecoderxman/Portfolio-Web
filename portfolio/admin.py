from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
# Register your models here.
from .models import stocks  
from .models import money
from .models import investments   
from .models import investmentsincommodities
from .models import investmentsinfunds
from .models import investmentsinindices
from .models import investmentsinbonds
from .models import investmentsinfutures

@admin.register(stocks,investments,money,investmentsincommodities,investmentsinfunds,investmentsinindices,investmentsinbonds,investmentsinfutures)
class ViewAdmin(ImportExportModelAdmin):
	pass