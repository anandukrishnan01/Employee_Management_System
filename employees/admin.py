from django.contrib import admin
from .models import EmployeeRecord


@admin.register(EmployeeRecord)
class EmployeeRecordAdmin(admin.ModelAdmin):
    list_display = ('data', 'template', 'created_by', 'created_at')
    search_fields = ('data',)
