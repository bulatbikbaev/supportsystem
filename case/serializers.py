from rest_framework.serializers import ModelSerializer

from .models import *


class CasesSerializer(ModelSerializer):
    class Meta:
        model = Cases
        fields = ['number', 'title', 'theme', 'type', 'start_job', 'end_job', 'status', 'authority', 'opened']


class DocumentSerializer(ModelSerializer):
    class Meta:
        model = Documents
        fields = ['type', 'status', 'added', 'case', 'file']