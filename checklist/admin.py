from django.contrib import admin
from .models import *

admin.site.register(MistakeTypes)
admin.site.register(Mistakes)
admin.site.register(Checklists)
admin.site.register(ChecklistStatus)
admin.site.register(Software)