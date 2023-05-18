from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from checklist.models import Checklists
from .serializers import *
from django.forms import model_to_dict
from rest_framework import generics
from rest_framework import status
import datetime
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.decorators import login_required
import threading
import docx
import os
from pdfminer.high_level import extract_text
import nltk
from nltk.corpus import stopwords
import string
from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer
from pymystem3 import Mystem
from nltk.probability import FreqDist
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import pymorphy3
import docx
import re
from django.core.files.base import ContentFile

# celery
from .tasks import execute_analysis


class CaseDocumentView(APIView):
    def post(self, request, case_number):
        """
        Добоавить документы к экспретизе с номером case_number
        """
        case_instance = Cases.objects.get(number=case_number)
        doc = Documents.objects.create(case=case_instance, file=request.data['new_document'],
                                       type=DocumentTypes.objects.get(title=request.data['document_type']))

        return Response(status=status.HTTP_201_CREATED)

    def get(self, request, case_number):
        """
        Получить документы экспретизы с номером case_number
        """
        case_instance = Cases.objects.get(number=case_number)
        if not case_instance:
            return Response(
                {"res": "Case with this case number does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        documents_instance = Documents.objects.filter(case=case_instance.id)

        print(documents_instance)
        if not documents_instance:
            return Response(
                {"res": "Documents with this case number does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        documents_serialized = DocumentSerializer(documents_instance, many=True)

        # Определяю тип работы по ключу и форматирую дату и время
        new_documents_serialized = list(documents_serialized.data)
        for d in new_documents_serialized:
            d['type'] = DocumentTypes.objects.get(id=d['type']).title
            temp_datetime = datetime.datetime.strptime(d['added'][:19], "%Y-%m-%dT%H:%M:%S")
            d['added'] = temp_datetime.strftime("%Y-%m-%d %H:%M")

        return Response({'documents': new_documents_serialized}, status=status.HTTP_200_OK)


class CaseView(APIView):
    permission_classes = [IsAuthenticated]

    """
    Создание экспертизы (подача заявки)
    """
    def post(self, request):
        print(request.data)
        today = datetime.datetime.now()
        case_new = Cases.objects.create(
            type=ProjectTypes.objects.get(title=request.data['type']),
            theme=Themes.objects.get(title=request.data['theme']),
            title=request.data['title'],
            opened=today,
            start_job=request.data['start_job'],
            end_job=request.data['end_job'],
        )

        # Сохранение загруженных файлов
        rep = Documents.objects.create(case=Cases.objects.get(id=case_new.id), file=request.data['report'],
                                       type=DocumentTypes.objects.get(title='Отчёт'))

        dec = Documents.objects.create(case=Cases.objects.get(id=case_new.id), file=request.data['declaration'],
                                       type=DocumentTypes.objects.get(title='Декларация'))

        spec = Documents.objects.create(case=Cases.objects.get(id=case_new.id), file=request.data['specification'],
                                        type=DocumentTypes.objects.get(title='Техническое задание'))

        ch = Checklists.objects.create(case=Cases.objects.get(id=case_new.id), report=Documents.objects.get(id=rep.id),
                                       specification=Documents.objects.get(id=spec.id),
                                       declaration=Documents.objects.get(id=dec.id))

        execute_analysis.delay(
            ch.id
        )

        # def async_function():
        #
        #     def getText(filename):  # Функция для получения текста документа формата .docx
        #         document = docx.Document(filename)
        #         fullText = []
        #         for para in document.paragraphs:
        #             fullText.append(para.text)
        #         return '\n'.join(fullText)
        #
        #     _, file_extension = os.path.splitext(ch.report.file.path)
        #     if file_extension == '.pdf':
        #         text = extract_text(ch.report.file.path)
        #     elif file_extension == '.docx' or '.doc':
        #         text = getText(ch.report.file.path)
        #
        #     text = text.lower()
        #     nltk.download("stopwords")
        #     punctuation = string.punctuation
        #     text = remove_chars_from_text(text, punctuation)
        #     text = remove_chars_from_text(text, string.digits)
        #     text_bin = text
        #
        #     tokenizer = RegexpTokenizer(r'\w+')
        #     text = tokenizer.tokenize(text)
        #     text = [i for i in text if i not in stopwords.words('russian')]
        #     text = [i for i in text if i not in stopwords.words('english')]
        #
        #     mystem_analyzer = Mystem()
        #     text = ' '.join([str(elem) for elem in text])
        #     text = mystem_analyzer.lemmatize(text)
        #     text = [w for w in text if (w != ' ')]
        #     text = nltk.Text(text)
        #     res = FreqDist(text)
        #     f = open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'media/documents/dict.txt'),
        #              encoding='utf-8')
        #     our_dict = []
        #     for line in f:
        #         our_dict.append(line[:-1])
        #     vocab = {}
        #     for k in our_dict:
        #         vocab[k] = text.count(k)
        #
        #     sorted_dict = {}
        #     sorted_keys = sorted(vocab, key=vocab.get, reverse=True)
        #
        #     for w in sorted_keys:
        #         sorted_dict[w] = vocab[w]
        #
        #     data = pd.DataFrame.from_dict(sorted_dict, orient='index', columns=['counts'])
        #     data_30 = data.head(30)
        #
        #     plt.figure(figsize=(26, 8))
        #     sns.barplot(data=data_30, x=(data_30.index), y=(data_30.counts))
        #     plt.xticks(rotation=45, fontsize=15)
        #     plt.yticks(fontsize=20)
        #     plt.ylabel('Количество', fontsize=20)
        #
        #     buffer2 = BytesIO()
        #     plt.savefig(buffer2, bbox_inches='tight')
        #     content_file2 = ContentFile(buffer2.getvalue())
        #     ch.report_diagram.save('diagramm', content_file2)
        #
        #     for i in ['цель', 'содержание', 'введение', 'основная часть', 'заключение', 'список исполнителей',
        #               'список источников|список использованных источников|список использованной литературы|список литературы',
        #               'приложение']:
        #         if (len(re.findall('\n {0,100}' + str(i) + ' {0,100}\n', text_bin)) >= 1):
        #             if str(i) == 'цель':
        #                 ch.has_purpose = True
        #                 ch.save(update_fields=["has_purpose"])
        #             if str(i) == 'содержание':
        #                 ch.has_content = True
        #                 ch.save(update_fields=["has_content"])
        #
        #             if str(i) == 'введение':
        #                 ch.has_introduction = True
        #                 ch.save(update_fields=["has_introduction"])
        #
        #             if str(i) == 'основная часть':
        #                 ch.has_main_part = True
        #                 ch.save(update_fields=["has_main_part"])
        #
        #             if str(i) == 'заключение':
        #                 ch.has_conclusion = True
        #                 ch.save(update_fields=["has_conclusion"])
        #
        #             if str(i) == 'список исполнителей':
        #                 ch.has_performers = True
        #                 ch.save(update_fields=["has_performers"])
        #
        #             if str(i) == 'список источников|список использованных источников|список использованной литературы|список литературы':
        #                 ch.has_sources = True
        #                 ch.save(update_fields=["has_sources"])
        #             if str(i) == 'приложение':
        #                 ch.has_application = True
        #                 ch.save(update_fields=["has_application"])
        #
        #     _, file_extension = os.path.splitext(ch.report.file.path)
        #     if file_extension == '.pdf':
        #         file = extract_text(ch.report.file.path)
        #     elif file_extension == '.docx':
        #         file = getText(ch.report.file.path)
        #
        #     def create_df(file):
        #         file = file.lower()
        #         text_bin = file
        #         tokenizer = RegexpTokenizer(r'\w+')
        #         text = tokenizer.tokenize(file)
        #
        #         text = [i for i in text if i not in stopwords.words('russian')]
        #         text = [i for i in text if i not in stopwords.words('english')]
        #
        #         file = remove_chars_from_text(file, string.punctuation)
        #         file = remove_chars_from_text(file, string.digits)
        #
        #         text = ' '.join([str(elem) for elem in text])
        #         nltk.download('punkt')
        #         text_tokens = word_tokenize(text)
        #         text = nltk.Text(text_tokens)
        #         fdist = FreqDist(text)
        #         df = pd.DataFrame(fdist.items(), columns=['word', 'count'])
        #         return text_bin, df
        #
        #     text, df = create_df(file)
        #
        #     def words_2(df):
        #         morph = pymorphy3.MorphAnalyzer()
        #         for i in range(len(df)):
        #             df.word[i] = morph.parse(df.word[i])[0].normal_form
        #         new_words = df.groupby(by=df.word, sort=False, as_index=False).sum()
        #         return new_words
        #
        #     new_df = words_2(df)
        #     data_words = pd.read_excel(
        #         os.path.join(os.path.dirname(os.path.dirname(__file__)), 'media/documents/dict_excel.xlsx'))
        #
        #     topics = {}
        #     for col in data_words:
        #         tmp = data_words[col]
        #         topics[col] = new_df.merge(tmp, how='inner', left_on='word', right_on=col)['count'].sum()
        #
        #     result_topic = max(topics, key=topics.get)
        #     ch.section_analyze = result_topic
        #     ch.save(update_fields=["section_analyze"])
        #
        # threading.Thread(target=async_function).start()
        #
        # print('ASYNC STARTED!')

        return Response({'case': model_to_dict(case_new)}, status=status.HTTP_201_CREATED)

    def get(self, request, case_number):
        """
        Получить экспертизу по case_number
        """
        case_instance = Cases.objects.get(number=case_number)
        if not case_instance:
            return Response(
                {"res": "Object with this case number does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        new_case_instance = model_to_dict(case_instance)
        new_case_instance['opened'] = new_case_instance['opened'].strftime("%Y-%m-%d %H:%M")
        new_case_instance['authority'] = TaxAuthorities.objects.get(id=new_case_instance['authority']).title
        new_case_instance['type'] = ProjectTypes.objects.get(id=new_case_instance['type']).title
        new_case_instance['status'] = CaseStatus.objects.get(id=new_case_instance['status']).title

        return Response({'case': new_case_instance}, status=status.HTTP_200_OK)


def remove_chars_from_text(text, chars):
    return "".join([ch for ch in text if ch not in chars])


def case_submit_page(request):
    # Передаю в контекст типы проектов (НИР, ОКР, НИОКР) для отображения в списке выбора
    # Передаю в контекст темы для отображения в списке выбора
    # Передаю today для ограничения выбора даты в календаре
    types_queryset = ProjectTypes.objects.all()
    theme_queryset = Themes.objects.all()
    context = {
        'today': f"{datetime.datetime.now():%Y-%m-%d}",
        'project_types': types_queryset,
        'themes': theme_queryset
    }

    return render(request, 'case_submit_page.html', context)


class CasesListView(APIView):
    """
    Список всех дел (экспертиз)
    """
    def get(self, request, format=None):
        queryset = Cases.objects.all()
        serializer_class = CasesSerializer(queryset, many=True)
        new_serializer_class = list(serializer_class.data)

        for c in new_serializer_class:
            c['type'] = ProjectTypes.objects.get(id=c['type']).title
            c['status'] = CaseStatus.objects.get(id=c['status']).title
            temp_datetime = datetime.datetime.strptime(c['opened'], "%Y-%m-%dT%H:%M:%S.%f")
            c['opened'] = temp_datetime.strftime("%Y-%m-%d %H:%M")

        return Response(new_serializer_class)



def cases_page(request):
    return render(request, 'cases_page.html')


def case_detail_page(request, case_number):
    context = {
        'case_number': case_number
    }

    return render(request, 'case_detail_page.html', context)


def document_add_page(request, case_number):
    doc_types_queryset = DocumentTypes.objects.all()
    context = {
        'case_number': case_number,
        'doc_types_queryset': doc_types_queryset
    }

    return render(request, 'document_add_page.html', context)
