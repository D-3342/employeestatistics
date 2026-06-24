# employees/migrations/0003_employeestatus_code_workday.py
import django.db.models.deletion
from django.db import migrations, models


def fill_status_codes(apps, schema_editor):
    EmployeeStatus = apps.get_model('employees', 'EmployeeStatus')
    mapping = {
        'Работает': 'Р',
        'В отпуске': 'О',
        'На больничном': 'Б',
        'Выходной': 'В',
        'Отсутствует по другой причине': 'Н',
    }
    for obj in EmployeeStatus.objects.all():
        obj.code = mapping.get(obj.name, 'Н')
        obj.save(update_fields=['code'])


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0002_alter_absencerecord_options_alter_department_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='employeestatus',
            name='code',
            field=models.CharField(max_length=1, null=True, blank=True, verbose_name='Код'),
        ),
        migrations.CreateModel(
            name='WorkDay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Дата')),
                ('hours', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Часы')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='workdays', to='employees.employee', verbose_name='Сотрудник')),
                ('status', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='employees.employeestatus', verbose_name='Статус')),
            ],
            options={
                'verbose_name': 'Рабочий день',
                'verbose_name_plural': 'Рабочие дни',
                'ordering': ['date'],
                'constraints': [models.UniqueConstraint(fields=('employee', 'date'), name='unique_employee_date_workday')],
            },
        ),
        migrations.RunPython(fill_status_codes, migrations.RunPython.noop),
    ]