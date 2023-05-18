from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, PermissionsMixin
from django.urls import reverse
from django.utils import timezone
from .managers import CustomUserManager



class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(unique=True, max_length=20, verbose_name='Логин (ИНН)')
    kpp = models.CharField(max_length=9, verbose_name='КПП', null=True, blank=True)
    title = models.CharField(max_length=100, verbose_name='Название компании', null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=15, verbose_name='Телефон', null=True, blank=True)
    is_staff = models.BooleanField(verbose_name='Является сотрудником', default=False)
    is_active = models.BooleanField(verbose_name='Активен', default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    head_full_name = models.CharField(max_length=200, verbose_name='ФИО руководителя', default='', null=True, blank=True)
    chief_accountant_full_name = models.CharField(max_length=200, verbose_name='ФИО главного бухгалтера', default='', null=True, blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    PAYER = 1
    EMPLOYEE = 2
    EXPERT = 3

    first_name = models.CharField('Имя', max_length=50, null=True, blank=True)
    last_name = models.CharField('Фамилия', max_length=50, null=True, blank=True)
    middle_name = models.CharField('Отчество', max_length=50, null=True, blank=True)

    ROLE_CHOICES = (
        (PAYER, 'Налогоплательщик'),
        (EMPLOYEE, 'Налоговый инспектор'),
        (EXPERT, 'Эксперт')
    )

    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True, default=1, verbose_name='Роль')

    objects = CustomUserManager()

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('profile', kwargs={'profile_inn': self.username})

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name plus the middle_name, with a space in between.
        '''
        full_name = '%s %s %s' % (self.last_name, self.first_name, self.middle_name)
        return full_name.strip()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'