# employees/migrations/0004_employeestatus_code_unique.py
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0003_employeestatus_code_workday'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeestatus',
            name='code',
            field=models.CharField(max_length=1, unique=True, verbose_name='Код'),
        ),
    ]