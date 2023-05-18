from dj_rest_auth.registration.views import RegisterView
from rest_framework import permissions
from .serializers import CustomRegisterSerializer, CustomEmpRegisterSerializer
from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy


class CustomRegisterView(RegisterView):
    """
    Регистрация налогоплательщика
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = CustomRegisterSerializer


def register_page(request):
    return render(request, 'register_page.html')


class CustomEmpRegisterView(RegisterView):
    """
    Регистрация налогового инспектора
    """
    serializer_class = CustomEmpRegisterSerializer
    permission_classes = [permissions.AllowAny]


def empregister_page(request):
    return render(request, 'empregister_page.html')


class LoginUser(LoginView):
    permission_classes = [permissions.AllowAny]
    template_name = 'login_page.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(LoginUser, self).get_context_data(**kwargs)
        context['title'] = 'Авторизация'
        return context

    def get_success_url(self):
        return reverse_lazy('home')


def home(request):
    return render(request, 'home_page.html', {'title': 'Главная страница'})