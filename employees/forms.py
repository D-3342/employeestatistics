from django import forms
from .models import Department, EmployeeStatus


class EmployeeFilterForm(forms.Form):
    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        required=False,
        empty_label='Все подразделения',
        label='Подразделение',
    )
    status = forms.ModelChoiceField(
        queryset=EmployeeStatus.objects.all(),
        required=False,
        empty_label='Все статусы',
        label='Статус',
    )