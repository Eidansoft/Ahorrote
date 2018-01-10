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
    return HttpResponseRedirect(
        reverse('add_tags', args=(",".join(selected),))
    )


def add_tags_with_regex(modeladmin, request, queryset):
    add_tags_with_regex.short_description = "Add tags to similar spendings ..."
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
    ordering = ['-date']


def graph_by_tag(modeladmin, request, queryset):
    graph_by_tag.short_description = 'View graph by tag (add)'
    selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
    return HttpResponseRedirect(
        reverse('graph_by_tags', args=(",".join(selected),))
    )


class TagAdministration(admin.ModelAdmin):
    actions = [graph_by_tag]


admin.site.register(Spending, SpendingAdministration)
admin.site.register(Tag, TagAdministration)
