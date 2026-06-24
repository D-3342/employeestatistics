import random
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker

from employees.models import Department, Position, EmployeeStatus, Employee, AbsenceRecord, WorkDay


class Command(BaseCommand):
    help = 'Заполняет базу данных тестовыми сотрудниками через Faker'

    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, default=30)
        parser.add_argument('--append', action='store_true')

    def handle(self, *args, **options):
        fake = Faker('ru_RU')
        count = options['count']
        append = options['append']

        department_names = [
            'Учебная часть', 'Бухгалтерия', 'Отдел кадров', 'Хозяйственный отдел',
            'Приёмная комиссия', 'IT-отдел', 'Библиотека',
            'Кафедра экономики и бухгалтерского учёта',
            'Кафедра права и правоохранительной деятельности',
            'Кафедра информационных систем и программирования',
            'Кафедра фармации', 'Кафедра логистики',
        ]

        position_names = [
            'Преподаватель', 'Старший преподаватель', 'Доцент', 'Заведующий кафедрой',
            'Лаборант', 'Методист', 'Бухгалтер', 'Главный бухгалтер',
            'Специалист отдела кадров', 'Завхоз', 'Системный администратор',
            'Программист', 'Разработчик веб-приложений', 'Библиотекарь',
            'Секретарь', 'Юрист', 'Фармацевт', 'Операционный логист',
        ]

        status_data = [
            ('Работает', 'success', 'Р'),
            ('В отпуске', 'warning', 'О'),
            ('На больничном', 'danger', 'Б'),
            ('Выходной', 'secondary', 'В'),
            ('Отсутствует по другой причине', 'info', 'Н'),
        ]

        if append:
            self.stdout.write('Добавляем сотрудников к существующим...')
        else:
            Employee.objects.all().delete()
            AbsenceRecord.objects.all().delete()
            WorkDay.objects.all().delete()

        departments = [Department.objects.get_or_create(name=name)[0] for name in department_names]
        positions = [Position.objects.get_or_create(name=name)[0] for name in position_names]
        statuses = []
        for name, color, code in status_data:
            status, _ = EmployeeStatus.objects.get_or_create(
                name=name,
                defaults={'color': color, 'code': code}
            )
            if status.color != color or status.code != code:
                status.color = color
                status.code = code
                status.save()
            statuses.append(status)

        comments_by_status = {
            'В отпуске': ['Отпуск по личным причинам', 'Ежегодный оплачиваемый отпуск', 'Учебный отпуск'],
            'На больничном': ['Грипп', 'ОРВИ', 'Бронхит', 'Ангина'],
            'Выходной': ['Выходной', 'Регулярный выходной', 'Дополнительный выходной'],
            'Отсутствует по другой причине': ['Личные причины', 'Командировка по учебе', 'Семейные обстоятельства'],
            'Работает': ['Рабочий день', 'На рабочем месте'],
        }

        self.stdout.write(f'Создаём {count} сотрудников...')

        created_employees = []
        for _ in range(count):
            employee = Employee.objects.create(
                full_name=fake.name(),
                position=random.choice(positions),
                department=random.choice(departments),
                current_status=random.choice(statuses),
                hire_date=fake.date_between(start_date='-8y', end_date='today'),
                phone=fake.phone_number(),
                email=fake.email(),
            )
            created_employees.append(employee)

        if not append:
            self.stdout.write('Создаём записи о периодах отсутствия/занятости...')

            today = timezone.now().date()

            for employee in created_employees:
                records_count = random.randint(1, 3)
                for i in range(records_count):
                    start = today - timedelta(days=random.randint(1, 365))
                    end = start + timedelta(days=random.randint(1, 14))
                    status = employee.current_status if i == records_count - 1 else random.choice(statuses)

                    AbsenceRecord.objects.create(
                        employee=employee,
                        status=status,
                        start_date=start,
                        end_date=end,
                        comment=random.choice(comments_by_status.get(status.name, [''])),
                    )

                for day in range(1, 29):
                    if random.random() < 0.7:
                        WorkDay.objects.create(
                            employee=employee,
                            date=today.replace(day=day),
                            status=random.choice(statuses),
                            hours=random.choice([4, 6, 8, 12]),
                        )

        self.stdout.write(self.style.SUCCESS(
            f'Готово! Создано: {len(created_employees)} сотрудников. '
            f'Всего в базе: {Employee.objects.count()} сотрудников, '
            f'{AbsenceRecord.objects.count()} записей истории, '
            f'{WorkDay.objects.count()} дневных записей.'
        ))