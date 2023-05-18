from django.db import models
from django.utils import timezone
from case.models import *

class MistakeTypes(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название недочёта')
    description = models.CharField(max_length=500, verbose_name='Описание')
    correction = models.CharField(max_length=500, verbose_name='Возможное исправление')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Тип недочёта'
        verbose_name_plural = 'Типы недочётов'


class ChecklistStatus(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Статус чек-листа'
        verbose_name_plural = 'Статусы чек-листов'


class Software(models.Model):
    title = models.TextField(verbose_name='Название', null=True, blank=True)
    other_title = models.TextField(verbose_name='Альтернативные названия', null=True, blank=True)
    software_class = models.TextField(verbose_name='Класс ПО', null=True, blank=True)
    software_code = models.TextField(verbose_name='Код продукции', null=True, blank=True)
    official_site = models.TextField(verbose_name='Сайт с документацией по установке и эксплуатации ПО', null=True, blank=True)
    owner = models.TextField(verbose_name='Правообладатель', null=True, blank=True)


class Checklists(models.Model):
    filled = models.DateTimeField(default=timezone.now, verbose_name='Дата и время заполнения')
    status = models.ForeignKey('ChecklistStatus', on_delete=models.PROTECT, verbose_name='Этап обработки', null=True, blank=True, default=1)
    case = models.ForeignKey(Cases, on_delete=models.PROTECT, verbose_name="Экспертиза", null=True, blank=True, related_name='case_checklist')
    report = models.ForeignKey(Documents, on_delete=models.PROTECT, verbose_name="Отчёт", null=True, blank=True, related_name='checklist_report')
    specification = models.ForeignKey(Documents, on_delete=models.PROTECT, verbose_name="Техническое задание", null=True, blank=True, related_name='checklist_specification')
    declaration = models.ForeignKey(Documents, on_delete=models.PROTECT, verbose_name="Декларация", null=True, blank=True, related_name='checklist_declaration')


    udk_index = models.CharField(max_length=1000, verbose_name='Индекс УДК по ГОСТ 7.90', null=True, blank=True)
    russ_class = models.CharField(max_length=1000, verbose_name='Коды Высших квалификационных группировок Общероссийского классификатора продукции', null=True, blank=True)
    numbers_report_ident = models.CharField(max_length=1000, verbose_name='Номера, идентифицирующие отчет', null=True, blank=True)
    report_type = models.CharField(max_length=1000, verbose_name='Вид отчета', null=True, blank=True)
    nir_maker = models.CharField(max_length=1000, verbose_name='Фамилии и инициалы исполнителей НИР', null=True, blank=True)
    maker_post = models.CharField(max_length=1000, verbose_name='Должности исполнителей НИР', null=True, blank=True)
    maker_degree = models.CharField(max_length=1000, verbose_name='Ученые степени исполнителей НИР', null=True, blank=True)
    maker_title = models.CharField(max_length=1000, verbose_name='Ученые звания исполнителей НИР', null=True, blank=True)
    report_place = models.CharField(max_length=1000, verbose_name='Место составления отчета', null=True, blank=True)
    report_date = models.DateField(verbose_name='Дата составления отчета', null=True, blank=True)

    page_count = models.IntegerField(verbose_name = 'Количество страниц', null=True, blank=True)
    application_count = models.IntegerField(verbose_name = 'Количество приложений', null=True, blank=True)
    source_count = models.IntegerField(verbose_name = 'Количество использованных источников', null=True, blank=True)

    key_words = models.CharField(max_length=1000, verbose_name='Перечень ключевых слов', null=True, blank=True)


    has_title_page = models.BooleanField(verbose_name="Есть титульная страница", null=True, blank=True)
    has_performers = models.BooleanField(verbose_name="Есть список исполнителей", null=True, blank=True)
    title_page_is_first = models.BooleanField(verbose_name="Титульная страница первая", null=True, blank=True)
    has_introduction = models.BooleanField(verbose_name="Есть введение", null=True, blank=True)
    has_main_part = models.BooleanField(verbose_name="Есть основная часть", null=True, blank=True)
    has_conclusion = models.BooleanField(verbose_name="Есть заключение", null=True, blank=True)
    has_application = models.BooleanField(verbose_name="Есть приложения", null=True, blank=True)
    has_purpose = models.BooleanField(verbose_name="Есть цель", null=True, blank=True)
    has_content = models.BooleanField(verbose_name="Есть содержание", null=True, blank=True)
    has_sources = models.BooleanField(verbose_name="Есть список источников", null=True, blank=True)
    section_analyze = models.CharField(max_length=500, verbose_name='Определенный по анализу раздел', null=True, blank=True)

    user_has_title_page = models.BooleanField(verbose_name="Есть титульная страница по мнению автора", null=True, blank=True)
    user_has_performers = models.BooleanField(verbose_name="Есть список исполнителей по мнению автора", null=True, blank=True)
    user_title_page_is_first = models.BooleanField(verbose_name="Титульная страница первая по мнению автора", null=True, blank=True)
    user_has_introduction = models.BooleanField(verbose_name="Есть введение по мнению автора", null=True, blank=True)
    user_has_main_part = models.BooleanField(verbose_name="Есть основная часть по мнению автора", null=True, blank=True)
    user_has_conclusion = models.BooleanField(verbose_name="Есть заключение по мнению автора", null=True, blank=True)
    user_has_application = models.BooleanField(verbose_name="Есть приложения по мнению автора", null=True, blank=True)
    user_has_purpose = models.BooleanField(verbose_name="Есть цель по мнению автора", null=True, blank=True)
    user_has_content = models.BooleanField(verbose_name="Есть содержание по мнению автора", null=True, blank=True)
    user_has_sources = models.BooleanField(verbose_name="Есть список источников по мнению автора", null=True, blank=True)

    is_gost = models.BooleanField(default=False, verbose_name="Отчет и документы по ГОСТУ", null=True, blank=True)
    is_first = models.BooleanField(default=False, verbose_name="работы являются впервые разработанными", null=True, blank=True)
    is_unique = models.BooleanField(default=False, verbose_name="работы направлены на создание нового уникального продукта", null=True, blank=True)
    exp_desc = models.BooleanField(default=False, verbose_name="отсутствовал опыт решения аналогичных задач", null=True, blank=True)
    contain_unique = models.BooleanField(default=False, verbose_name="работы содержат в качестве предмета или объекта труда уникальные инновационные инструменты", null=True, blank=True)
    contain_experiment = models.BooleanField(default=False, verbose_name="работы содержат в себе признаки экспериментальных разработок ", null=True, blank=True)
    efficient_nec = models.BooleanField(default=False, verbose_name="работы не обусловлены необходимостью повышения эффективности операционной деятельности телекоммуникационных компаний", null=True, blank=True)
    integration = models.BooleanField(default=False, verbose_name="работы не характерны для типового внедренческого проекта по системной интеграции существующих решений", null=True, blank=True)

    risk = models.BooleanField(default=False, verbose_name="работы имели высокие проектные и технологические риски", null=True, blank=True)
    used = models.BooleanField(default=False, verbose_name="примененные решения не основаны на общеизвестных способах", null=True, blank=True)
    union = models.BooleanField(default=False, verbose_name="работы не являются объединением общеизвестных технологий и алгоритмов", null=True, blank=True)
    modification = models.BooleanField(default=False, verbose_name="не осуществлялась настройка/ доработка/ модификация ранее известных технологий", null=True, blank=True)
    analog = models.BooleanField(default=False, verbose_name="не существуют общедоступные аналоги", null=True, blank=True)
    new_knowledge = models.BooleanField(default=False, verbose_name="не являются решением технических или инженерных задач по адаптации решения для работы в виртуальной среде", null=True, blank=True)
    # report_line = models.ImageField(upload_to="documents/%Y/%m/%d/", verbose_name="Линейный график", null=True, blank=True)
    report_diagram = models.ImageField(upload_to="documents/%Y/%m/%d/", verbose_name="Гистограмма", null=True, blank=True)
    # report_pie = models.ImageField(upload_to="documents/%Y/%m/%d/", verbose_name="Круговая диаграмма", null=True, blank=True)
    adopted = models.BooleanField(default=False, verbose_name="Работа принята", null=True, blank=True)
    comment = models.CharField(max_length=1000, verbose_name='Комментарий', null=True, blank=True)
    software = models.TextField(verbose_name="Использованные программы", null=True, blank=True)

    class Meta:
        verbose_name = 'Чек-лист'
        verbose_name_plural = 'Чек-листы'

    def get_absolute_url(self):
        return f'/checklist/{self.case.number}/'

    def get_absolute_url_main(self):
        return f'/checklist/main/{self.case.number}/'

class Mistakes(models.Model):
    checklist = models.ForeignKey('Checklists', on_delete=models.PROTECT, verbose_name="Чек-лист", null=True, blank=True)
    mistake = models.ForeignKey('MistakeTypes', on_delete=models.PROTECT, verbose_name="Недочёт", null=True, blank=True)

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = 'Недочёт'
        verbose_name_plural = 'Недочёты'

