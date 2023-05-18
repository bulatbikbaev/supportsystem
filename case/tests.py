from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient
from .models import *
from checklist.models import *
import datetime

# Тестирование подачи заявки
class CaseViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = '/api/case/'
        self.user = get_user_model().objects.create_user(username='12345678910', password='testpassword')
        self.client.force_authenticate(user=self.user)

        # Создаю записей - внешних ключей для модели экспертизы
        dt1 = DocumentTypes(title="Отчёт")
        dt1.save()

        dt2 = DocumentTypes(title="Декларация")
        dt2.save()

        dt3 = DocumentTypes(title="Техническое задание")
        dt3.save()

        ch_status = ChecklistStatus(title="Status 1")
        ch_status.save()

        section = Section(title="Section 1")
        section.save()

        type = ProjectTypes(title="Type 1")
        type.save()

        status = CaseStatus(code="1", title="Status 1")
        status.save()

        tax_auth = TaxAuthorities(code="1", title="Tax 1")
        tax_auth.save()

        theme = Themes(title="Theme 1", section=Section.objects.get(title="Section 1"))
        theme.save()

    def test_create_case_success(self):
        data = {
            'type': 'Type 1',
            'theme': 'Theme 1',
            'title': 'Test Case',
            'start_job': '2023-05-10',
            'end_job': '2023-05-15',
            'report': 'report_file_content',
            'declaration': 'declaration_file_content',
            'specification': 'specification_file_content'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['case']['title'], 'Test Case')

    def test_create_case_unauthenticated(self):
        self.client.logout()
        data = {
            'type': 'Type 1',
            'theme': 'Theme 1',
            'title': 'Test Case',
            'start_job': '2023-05-10',
            'end_job': '2023-05-15',
            'report': 'report_file_content',
            'declaration': 'declaration_file_content',
            'specification': 'specification_file_content'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 401)


class CasesListViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = '/api/cases/'

        type = ProjectTypes(title="Type 1")
        type.save()

        status = CaseStatus(code="1", title="Status 1")
        status.save()

        tax_auth = TaxAuthorities(code="1", title="Tax 1")
        tax_auth.save()

    def test_get_cases_list_success(self):
        # Создаем тестовые объекты Cases и связанные объекты ProjectTypes и CaseStatus
        case = Cases.objects.create(
            type=ProjectTypes.objects.get(title="Type 1"),
            status=CaseStatus.objects.get(title="Status 1"),
            opened=datetime.datetime.now(),
            # Добавьте остальные поля, необходимые для создания Cases
        )

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        cases_data = response.data

        self.assertEqual(len(cases_data), 1)  # Проверяем, что получен список с одним делом
        case_data = cases_data[0]

        # Проверяем, что данные дела соответствуют ожидаемым значениям
        self.assertEqual(case_data['number'], case.number)
        self.assertEqual(case_data['type'], "Type 1")
        self.assertEqual(case_data['status'], "Status 1")
