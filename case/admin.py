from django.contrib import admin
from .models import *

admin.site.register(DocumentTypes)
admin.site.register(ProjectTypes)
admin.site.register(Documents)
admin.site.register(DocumentStatus)
admin.site.register(CaseStatus)
admin.site.register(Cases)
admin.site.register(Messages)
admin.site.register(Themes)
admin.site.register(TaxAuthorities)
admin.site.register(Section)


# Register your models here.
