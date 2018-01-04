# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from django.contrib import admin
from django.urls import reverse
from .models import Spending, Tag


# Register your models here.
def add_tags(modeladmin, request, queryset):
    add_tags.short_description = "Add tags ..."
    selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
    ct = ContentType.objects.get_for_model(queryset.model)
    return HttpResponseRedirect(reverse('add_tags', args=(ct.pk, ",".join(selected))))


class SpendingAdministration(admin.ModelAdmin):
    list_display = ('date', 'concept', 'amount')
    list_filter = ['tags']
    search_fields = ['concept']
    actions = [add_tags]


admin.site.register(Spending, SpendingAdministration)
admin.site.register(Tag)
