# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
import csv, json
from gastos.models import Spending, Tag
from gastos.forms import TagsForm, SpendingConceptRegexSearchForm


# Create your views here.
def add_tags_view(request, spending_ids):
    '''View that let the user provide a list of tags to apply
       to a provided (by GET) list of spendings'''
    context = {}
    context['form'] = TagsForm(initial={'spending_ids': spending_ids})
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
            messages.add_message(
                request, messages.ERROR,
                'No valid data provided.'
            )

    return render(request, 'gastos/add_tags.html', context)


def add_tags_with_regex_view(request, spending_id):
    '''View that let the user to create a regex that match all
       wanted spendings; in order to apply lately the desired
       tags.'''
    objs = {}
    if request.method == 'GET':
        # main entry point
        spending = Spending.objects.get(pk=spending_id)
        concept_regex = '^{}$'.format(
            spending.concept
            .replace('(', '\(')
            .replace(')', '\)')
            .replace('.', '\.')
            .replace('*', '\*')
        )
        form = SpendingConceptRegexSearchForm(
            initial={'regex': concept_regex}
        )
        objs = Spending.objects.filter(
            concept__iregex=concept_regex
        )

    elif request.method == 'POST':
        # search a regex expression
        form = SpendingConceptRegexSearchForm(request.POST)
        if form.is_valid():
            objs = Spending.objects.filter(concept__iregex=form.data['regex'])
            return render(
                request, 'gastos/search_spends_by_regex.html',
                get_context_for_add_tags_with_regex(form, objs)
            )
        else:
            messages.add_message(
                request, messages.ERROR,
                'No valid data provided.'
            )

    return render(
        request, 'gastos/search_spends_by_regex.html',
        get_context_for_add_tags_with_regex(form, objs)
    )


def get_context_for_add_tags_with_regex(form, objs):
    context = {}
    context['message'] = 'Create and test the regex, ' \
        'when you are ready, continue to apply tags:'
    context['spending_list'] = objs
    spending_ids_array = [s.pk for s in objs]
    context['spending_ids'] = ','.join(map(str, spending_ids_array))
    context['form'] = form
    return context



def list_tags_json(request):
    '''Return a list with all tag names in text/json format. The idea for
       this is to use it as ajax data'''
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
