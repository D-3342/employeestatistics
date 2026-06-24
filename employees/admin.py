from django.contrib import admin
from .models import Department, Position, EmployeeStatus, Employee, AbsenceRecord, WorkDay


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(EmployeeStatus)
class EmployeeStatusAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'color')
    search_fields = ('code', 'name')


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'position', 'department', 'current_status', 'hire_date')
    search_fields = ('full_name',)


@admin.register(AbsenceRecord)
class AbsenceRecordAdmin(admin.ModelAdmin):
    list_display = ('employee', 'status', 'start_date', 'end_date')
    list_filter = ('status',)


@admin.register(WorkDay)
class WorkDayAdmin(admin.ModelAdmin):
    list_display = ('employee', 'date', 'status', 'hours')
    list_filter = ('status', 'date')
    search_fields = ('employee__full_name',)