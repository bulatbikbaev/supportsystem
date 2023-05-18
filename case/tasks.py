from time import sleep

from celery import shared_task
from django.core.mail import send_mail
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
from checklist.models import *


@shared_task()
def execute_analysis(ch_id):
    ch = Checklists.objects.get(id=ch_id)

    def remove_chars_from_text(text, chars):
        return "".join([ch for ch in text if ch not in chars])

    def getText(filename):  # Функция для получения текста документа формата .docx
        document = docx.Document(filename)
        fullText = []
        for para in document.paragraphs:
            fullText.append(para.text)
        return '\n'.join(fullText)

    _, file_extension = os.path.splitext(ch.report.file.path)
    if file_extension == '.pdf':
        text = extract_text(ch.report.file.path)
    elif file_extension == '.docx' or '.doc':
        text = getText(ch.report.file.path)

    text = text.lower()
    nltk.download("stopwords")
    punctuation = string.punctuation
    text = remove_chars_from_text(text, punctuation)
    text = remove_chars_from_text(text, string.digits)
    text_bin = text

    tokenizer = RegexpTokenizer(r'\w+')
    text = tokenizer.tokenize(text)
    text = [i for i in text if i not in stopwords.words('russian')]
    text = [i for i in text if i not in stopwords.words('english')]

    mystem_analyzer = Mystem()
    text = ' '.join([str(elem) for elem in text])
    text = mystem_analyzer.lemmatize(text)
    text = [w for w in text if (w != ' ')]
    text = nltk.Text(text)
    res = FreqDist(text)
    f = open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'media/documents/dict.txt'),
             encoding='utf-8')
    our_dict = []
    for line in f:
        our_dict.append(line[:-1])
    vocab = {}
    for k in our_dict:
        vocab[k] = text.count(k)

    sorted_dict = {}
    sorted_keys = sorted(vocab, key=vocab.get, reverse=True)

    for w in sorted_keys:
        sorted_dict[w] = vocab[w]

    data = pd.DataFrame.from_dict(sorted_dict, orient='index', columns=['counts'])
    data_30 = data.head(30)

    plt.figure(figsize=(26, 8))
    sns.barplot(data=data_30, x=(data_30.index), y=(data_30.counts))
    plt.xticks(rotation=45, fontsize=15)
    plt.yticks(fontsize=20)
    plt.ylabel('Количество', fontsize=20)

    buffer2 = BytesIO()
    plt.savefig(buffer2, bbox_inches='tight')
    content_file2 = ContentFile(buffer2.getvalue())
    ch.report_diagram.save('diagramm', content_file2)

    for i in ['цель', 'содержание', 'введение', 'основная часть', 'заключение', 'список исполнителей',
              'список источников|список использованных источников|список использованной литературы|список литературы',
              'приложение']:
        if (len(re.findall('\n {0,100}' + str(i) + ' {0,100}\n', text_bin)) >= 1):
            if str(i) == 'цель':
                ch.has_purpose = True
                ch.save(update_fields=["has_purpose"])
            if str(i) == 'содержание':
                ch.has_content = True
                ch.save(update_fields=["has_content"])

            if str(i) == 'введение':
                ch.has_introduction = True
                ch.save(update_fields=["has_introduction"])

            if str(i) == 'основная часть':
                ch.has_main_part = True
                ch.save(update_fields=["has_main_part"])

            if str(i) == 'заключение':
                ch.has_conclusion = True
                ch.save(update_fields=["has_conclusion"])

            if str(i) == 'список исполнителей':
                ch.has_performers = True
                ch.save(update_fields=["has_performers"])

            if str(i) == 'список источников|список использованных источников|список использованной литературы|список литературы':
                ch.has_sources = True
                ch.save(update_fields=["has_sources"])
            if str(i) == 'приложение':
                ch.has_application = True
                ch.save(update_fields=["has_application"])

    _, file_extension = os.path.splitext(ch.report.file.path)
    if file_extension == '.pdf':
        file = extract_text(ch.report.file.path)
    elif file_extension == '.docx':
        file = getText(ch.report.file.path)

    def create_df(file):
        file = file.lower()
        text_bin = file
        tokenizer = RegexpTokenizer(r'\w+')
        text = tokenizer.tokenize(file)

        text = [i for i in text if i not in stopwords.words('russian')]
        text = [i for i in text if i not in stopwords.words('english')]

        file = remove_chars_from_text(file, string.punctuation)
        file = remove_chars_from_text(file, string.digits)

        text = ' '.join([str(elem) for elem in text])
        nltk.download('punkt')
        text_tokens = word_tokenize(text)
        text = nltk.Text(text_tokens)
        fdist = FreqDist(text)
        df = pd.DataFrame(fdist.items(), columns=['word', 'count'])
        return text_bin, df

    text, df = create_df(file)

    def words_2(df):
        morph = pymorphy3.MorphAnalyzer()
        for i in range(len(df)):
            df.word[i] = morph.parse(df.word[i])[0].normal_form
        new_words = df.groupby(by=df.word, sort=False, as_index=False).sum()
        return new_words

    new_df = words_2(df)
    data_words = pd.read_excel(
        os.path.join(os.path.dirname(os.path.dirname(__file__)), 'media/documents/dict_excel.xlsx'))

    topics = {}
    for col in data_words:
        tmp = data_words[col]
        topics[col] = new_df.merge(tmp, how='inner', left_on='word', right_on=col)['count'].sum()

    result_topic = max(topics, key=topics.get)
    ch.section_analyze = result_topic
    ch.save(update_fields=["section_analyze"])

