from django.contrib import admin

# Register your models here.

from .models import Case, Slagningar
admin.site.register(Case)
admin.site.register(Slagningar)
