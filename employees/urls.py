from django.urls import path
from . import views

app_name = 'employees'

urlpatterns = [
    path('', views.home, name='home'),
    path('employees/', views.employee_list, name='employee_list'),
    path('employees/<int:pk>/', views.employee_detail, name='employee_detail'),
    path('employees/<int:pk>/calendar/', views.employee_calendar_api, name='employee_calendar_api'),
    path('employees/<int:pk>/calendar/day/', views.employee_calendar_day_api, name='employee_calendar_day_api'),
    path('timesheets/', views.timesheet_index, name='timesheet_index'),
    path('about/', views.about, name='about'),
]