from django.db import models


class Department(models.Model):
    """Подразделение техникума (например, бухгалтерия, учебная часть)."""

    name = models.CharField('Название подразделения', max_length=150, unique=True)

    class Meta:
        verbose_name = 'Подразделение'
        verbose_name_plural = 'Подразделения'
        ordering = ['name']

    def __str__(self):
        return self.name


class Position(models.Model):
    """Должность сотрудника (например, преподаватель, лаборант)."""

    name = models.CharField('Название должности', max_length=150, unique=True)

    class Meta:
        verbose_name = 'Должность'
        verbose_name_plural = 'Должности'
        ordering = ['name']

    def __str__(self):
        return self.name


class EmployeeStatus(models.Model):
    """Статус сотрудника: работает, в отпуске, на больничном и т.д."""

    name = models.CharField('Название статуса', max_length=50, unique=True)
    color = models.CharField(
        'Цвет метки',
        max_length=20,
        default='secondary',
        help_text="Например: success, warning, danger, info, secondary (Bootstrap-классы)"
    )

    class Meta:
        verbose_name = 'Статус сотрудника'
        verbose_name_plural = 'Статусы сотрудников'
        ordering = ['name']

    def __str__(self):
        return self.name


class Employee(models.Model):
    """Сотрудник техникума."""

    full_name = models.CharField('ФИО', max_length=200)
    position = models.ForeignKey(
        Position,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='employees',
        verbose_name='Должность',
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='employees',
        verbose_name='Подразделение',
    )
    current_status = models.ForeignKey(
        EmployeeStatus,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='employees',
        verbose_name='Текущий статус',
    )
    hire_date = models.DateField('Дата приёма на работу', null=True, blank=True)

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'
        ordering = ['full_name']

    def __str__(self):
        return self.full_name


class AbsenceRecord(models.Model):
    """Запись о периоде отсутствия или занятости сотрудника."""

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='absence_records',
        verbose_name='Сотрудник',
    )
    status = models.ForeignKey(
        EmployeeStatus,
        on_delete=models.CASCADE,
        related_name='absence_records',
        verbose_name='Статус периода',
    )
    start_date = models.DateField('Дата начала')
    end_date = models.DateField('Дата окончания', null=True, blank=True)
    comment = models.CharField('Комментарий', max_length=255, blank=True)

    class Meta:
        verbose_name = 'Запись о периоде'
        verbose_name_plural = 'Записи о периодах'
        ordering = ['-start_date']

    def __str__(self):
        return f'{self.employee.full_name} — {self.status.name} ({self.start_date})'