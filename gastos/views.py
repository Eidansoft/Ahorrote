# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse
import csv, json
from gastos.models import Spending, Tag
from gastos.forms import TagsForm


# Create your views here.
def add_tags(request, ct, ids):
    context = {}
    context['form'] = TagsForm(initial={'spending_ids': ids})
    if request.method == 'GET':
        # main entry point
        context['message'] = 'Write the tags to add.'

    elif request.method == 'POST':
        # validation and apply changes
        form = TagsForm(request.POST)
        if form.is_valid():
            for spending_id in form.data['spending_ids'].split(','):
                spend = Spending.objects.get(pk=spending_id)
                for tag_name in form.data['tags'].split(','):
                    tag, created = Tag.objects.get_or_create(name=tag_name)
                    if not spend.tags.all().filter(name=tag_name):
                        spend.tags.add(tag)
            messages.add_message(request, messages.INFO, 'Tags applied!')
            return HttpResponseRedirect('/admin/gastos/spending/')
        else:
            messages.add_message(request, messages.ERROR, 'No valid data.')

    return render(request, 'gastos/add_tags.html', context)


def list_tags(request):
    tag_names = [t.name for t in Tag.objects.all()]
    return HttpResponse(json.dumps(tag_names), content_type='text/json')


def filter_by_concept(request, pattern):
    objs = Spending.objects.filter(concept__iregex=pattern)
    return spending_list_to_csv_response(objs)


def spending_list_to_csv_response(objs):
    response = HttpResponse(content_type='text/csv')
    # response['Content-Disposition'] = 'attachment; filename="data.csv"'

    writer = csv.writer(response)

    fieldnames = ['date', 'concept', 'amount']
    writer.writerow(fieldnames)

    for obj in objs:
        writer.writerow([obj.date, obj.concept, obj.amount])

    return response
