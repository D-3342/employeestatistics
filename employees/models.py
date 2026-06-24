from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=200, unique=True, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Подразделение'
        verbose_name_plural = 'Подразделения'


class Position(models.Model):
    name = models.CharField(max_length=200, unique=True, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Должность'
        verbose_name_plural = 'Должности'


class EmployeeStatus(models.Model):
    code = models.CharField(max_length=1, unique=True, verbose_name='Код')
    name = models.CharField(max_length=100, unique=True, verbose_name='Название')
    color = models.CharField(max_length=20, verbose_name='Цвет бейджа')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'


class Employee(models.Model):
    full_name = models.CharField(max_length=200, verbose_name='ФИО')
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Должность')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Подразделение')
    current_status = models.ForeignKey(EmployeeStatus, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Текущий статус')
    hire_date = models.DateField(null=True, blank=True, verbose_name='Дата приёма')
    phone = models.CharField(max_length=20, blank=True, verbose_name='Телефон')
    email = models.EmailField(blank=True, verbose_name='Email')

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'
        ordering = ['full_name']


class AbsenceRecord(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name='Сотрудник')
    status = models.ForeignKey(EmployeeStatus, on_delete=models.CASCADE, verbose_name='Статус')
    start_date = models.DateField(verbose_name='Дата начала')
    end_date = models.DateField(null=True, blank=True, verbose_name='Дата окончания')
    comment = models.TextField(blank=True, verbose_name='Комментарий')

    def __str__(self):
        return f'{self.employee.full_name} — {self.status.name}'

    class Meta:
        verbose_name = 'Период отсутствия'
        verbose_name_plural = 'Периоды отсутствия'
        ordering = ['-start_date']


class WorkDay(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='workdays', verbose_name='Сотрудник')
    date = models.DateField(verbose_name='Дата')
    status = models.ForeignKey(EmployeeStatus, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Статус')
    hours = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='Часы')

    def __str__(self):
        return f'{self.employee.full_name} — {self.date}'

    class Meta:
        verbose_name = 'Рабочий день'
        verbose_name_plural = 'Рабочие дни'
        constraints = [
            models.UniqueConstraint(fields=['employee', 'date'], name='unique_employee_date_workday')
        ]
        ordering = ['date']