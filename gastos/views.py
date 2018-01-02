# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
import csv
from gastos.models import Spending


# Create your views here.
def add_tags(request, ct, ids):
    import ipdb; ipdb.set_trace(context=21)
    return None


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
