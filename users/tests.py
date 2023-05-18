from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient


# Тестирование регистрации нового пользователя
class RegistrationTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = '/api/registration/'

    def test_registration_success(self):
        data = {
            'title': 'Test Company',
            'username': '12345678910',
            'kpp': '123456789',
            'email': 'test@example.com',
            'password1': 'testpassword',
            'password2': 'testpassword',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(get_user_model().objects.count(), 1)
        self.assertEqual(get_user_model().objects.get().username, '12345678910')


# Тестирование аутентификации пользователя
class AuthenticationTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = '/api/login/'
        self.user = get_user_model().objects.create_user(username='12345678910', password='testpassword')

    def test_authentication_success(self):
        data = {
            'username': '12345678910',
            'password': 'testpassword',
        }
        response = self.client.post(self.url, data)
        # Проверка кода ответа
        self.assertEqual(response.status_code, 200)
        # Проверка наличия токенов в ответе
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)


# Тестирование выхода пользователя
class LogoutTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = '/api/logout/'
        self.user = get_user_model().objects.create_user(username='12345678910', password='testpassword')
        self.client.force_authenticate(user=self.user)

    def test_logout_success(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('my-app-auth', self.client.session)
