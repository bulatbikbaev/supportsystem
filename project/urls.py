"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from case.views import *
from django.conf.urls.static import static
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.urls import path, include, re_path
from allauth.account.views import confirm_email
from users.views import *

schema_view = get_schema_view(
   openapi.Info(
      title="Support System API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    # ADMIN
    path('admin/', admin.site.urls),

    # APPS
    path('', home, name='home'),
    path('case_submit/', case_submit_page),
    path('cases/', cases_page),
    path('case/<int:case_number>/', case_detail_page, name='case_detail_page'),
    path('case/<int:case_number>/document/', document_add_page, name='document_add_page'),

    path('login/', LoginUser.as_view()),
    path('register/', register_page),
    path('empregister/', empregister_page),

    # API
    path('api/cases/', CasesListView.as_view(), name='case_list'),
    path('api/case/<int:case_number>/', CaseView.as_view(), name='case_detail'),
    path('api/case/', CaseView.as_view(), name='submit_case'),
    path('api/case/documents/<int:case_number>/', CaseDocumentView.as_view(), name='case_documents'),

    # AUTH API
    path('accounts/', include('allauth.urls')),
    path('api/', include('dj_rest_auth.urls')),
    path('api/registration/', CustomRegisterView.as_view(), name='register'),
    path('api/empregistration/', CustomEmpRegisterView.as_view(), name='emp_register'),

    # Swagger
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # Prometeus
    path('prometheus/', include('django_prometheus.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
