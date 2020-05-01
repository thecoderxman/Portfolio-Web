from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
# Register your models here.
from .models import stocks  
from .models import money
from .models import investments   
@admin.register(stocks,investments,money)
class ViewAdmin(ImportExportModelAdmin):
	pass