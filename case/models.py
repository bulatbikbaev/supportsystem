from django.db import models
from django.utils import timezone
import random
import datetime
from django.conf import settings
from users.models import CustomUser


class TaxAuthorities(models.Model):
    code = models.CharField(max_length=4, verbose_name='Код')
    title = models.CharField(max_length=200, verbose_name='Название')

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = 'Налоговый орган'
        verbose_name_plural = 'Налоговые органы'


class Section(models.Model):
    title = models.CharField(max_length=400, verbose_name='Название')

    class Meta:
        verbose_name = 'Раздел'
        verbose_name_plural = 'Разделы'

    def __str__(self):
        return self.title


class ProjectTypes(models.Model):
    title = models.CharField(max_length=10, verbose_name='Название')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Тип проекта'
        verbose_name_plural = 'Типы проектов'


class DocumentTypes(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Тип документа'
        verbose_name_plural = 'Типы документов'


class Themes(models.Model):
    title = models.CharField(max_length=300, verbose_name='Название')
    section = models.ForeignKey(Section, on_delete=models.PROTECT, verbose_name="Раздел", related_name="theme_section", null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Тема'
        verbose_name_plural = 'Темы'

    def get_theme_section(self):
        return self.title + ' из раздела ' + self.section.__str__()


class DocumentStatus(models.Model):
    title = models.CharField(max_length=50, verbose_name='Название')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Статус документа'
        verbose_name_plural = 'Статусы документов'




class CaseStatus(models.Model):
    code = models.IntegerField(verbose_name = 'Номер', null=True, blank=True)
    title = models.CharField(max_length=200, verbose_name='Название')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Статус дела'
        verbose_name_plural = 'Статусы дел'

def random_string():
    return str(random.randint(10000, 99999))

class Cases(models.Model):
    number = models.CharField(max_length=10, verbose_name='Номер дела', default=random_string)
    payer = models.ForeignKey(CustomUser, on_delete=models.PROTECT, verbose_name="Налогоплательщик", related_name="case_payer", null=True, blank=True)
    employee = models.ForeignKey(CustomUser, on_delete=models.PROTECT, verbose_name="Налоговый инспектор", null=True, blank=True)
    type = models.ForeignKey('ProjectTypes', on_delete=models.PROTECT, verbose_name='Тип проекта', related_name="case_type", null=True, blank=True)
    title = models.CharField(max_length=300, verbose_name='Наименование работы')
    theme = models.ForeignKey('Themes', on_delete=models.PROTECT, verbose_name='Тема', null=True, blank=True)
    opened = models.DateTimeField(default=timezone.now, verbose_name='Открыто')
    closed = models.DateTimeField(verbose_name='Закрыто', null=True, blank=True)

    start_job = models.DateField(verbose_name='Начало выполнения работ', null=True, blank=True)
    end_job = models.DateField(verbose_name='Конец выполнения работ', null=True, blank=True)

    authority = models.ForeignKey('TaxAuthorities', on_delete=models.PROTECT, verbose_name='Налоговый орган', null=True, blank=True, default=1)
    status = models.ForeignKey('CaseStatus', on_delete=models.SET_NULL, blank=True, null=True, default=1, verbose_name='Статус экспертизы')



    def __str__(self):
        return self.number

    class Meta:
        verbose_name = 'Налоговое дело'
        verbose_name_plural = 'Налоговые дела'


class Documents(models.Model):
    type = models.ForeignKey('DocumentTypes', on_delete=models.PROTECT, verbose_name='Тип документа', null=True, blank=True)
    status = models.ForeignKey('DocumentStatus', on_delete=models.PROTECT, verbose_name='Статус', null=True, blank=True)
    added = models.DateTimeField(default=timezone.now)
    case = models.ForeignKey('Cases', on_delete=models.PROTECT, verbose_name='Дело', related_name='documents')
    file = models.FileField(upload_to="documents/%Y/%m/%d/", verbose_name="Файл")

    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'

    def __str__(self):
        s = " ".join([self.case.__str__(),self.type.__str__()])
        return s



class Messages(models.Model):
    case = models.ForeignKey('Cases', on_delete=models.PROTECT, verbose_name='Дело')
    added = models.DateTimeField(default=timezone.now)
    text = models.CharField(max_length=200, verbose_name='Сообщение')
    sender = models.ForeignKey(CustomUser, on_delete=models.PROTECT, verbose_name="Отправитель", related_name="sender", null=True, blank=True)

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
