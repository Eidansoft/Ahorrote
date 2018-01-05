# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponseRedirect
from django.contrib import admin, messages
from django.urls import reverse
from .models import Spending, Tag


# Register your models here.
def add_tags(modeladmin, request, queryset):
    add_tags.short_description = "Add tags ..."
    selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
    return HttpResponseRedirect(reverse('add_tags', args=(",".join(selected))))


def add_tags_with_regex(modeladmin, request, queryset):
    add_tags_with_regex.short_description = "Add tags to similar spendings ..."
    import ipdb; ipdb.set_trace(context=21)
    selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
    if len(selected) > 1:
        messages.add_message(
            request, messages.WARNING,
            'Please choose only a single spending.'
        )
        return HttpResponseRedirect('/admin/gastos/spending/')
    return HttpResponseRedirect(
        reverse('add_tags_with_regex', args=(selected[0],))
    )


class SpendingAdministration(admin.ModelAdmin):
    list_display = ('date', 'concept', 'amount')
    list_filter = ['tags']
    search_fields = ['concept']
    actions = [add_tags, add_tags_with_regex]


admin.site.register(Spending, SpendingAdministration)
admin.site.register(Tag)
