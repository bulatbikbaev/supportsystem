# serializers.py in the users Django app
from django.db import transaction
from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer


class CustomRegisterSerializer(RegisterSerializer):
    username = serializers.CharField(max_length=20)
    kpp = serializers.CharField(max_length=9)
    title = serializers.CharField(max_length=100)

    @transaction.atomic
    def save(self, request):
        user = super().save(request)
        user.username = self.data.get('username')
        user.kpp = self.data.get('kpp')
        user.title = self.data.get('title')
        user.save()
        return user


class CustomEmpRegisterSerializer(RegisterSerializer):
    username = serializers.CharField(max_length=20)
    last_name = serializers.CharField(max_length=50)
    first_name = serializers.CharField(max_length=50)
    middle_name = serializers.CharField(max_length=50)
    @transaction.atomic
    def save(self, request):
        user = super().save(request)
        user.username = self.data.get('username')
        user.last_name = self.data.get('last_name')
        user.first_name = self.data.get('first_name')
        user.middle_name = self.data.get('middle_name')

        # Установка роли налогового инспектора (2 в списке)
        user.role = 2
        user.save()
        return user

