from django.contrib import admin

# Register your models here.
from .models import Graph, CaseData
#admin.site.register(Processes)
admin.site.register(Graph)
admin.site.register(CaseData)