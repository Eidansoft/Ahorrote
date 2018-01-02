# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Spending, Tag


# Register your models here.
class SpendingAdministration(admin.ModelAdmin):
    list_display = ('date', 'concept', 'amount')
    list_filter = ['tags']
    search_fields = ['concept']


admin.site.register(Spending, SpendingAdministration)
admin.site.register(Tag)
