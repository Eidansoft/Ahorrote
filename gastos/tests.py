# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from gastos.models import Spending, Tag
from django.test import TestCase
from datetime import datetime, timedelta


# Create your tests here.
class GastosTests(TestCase):
    def setUp(self):
        self.tag_names = ['tag 1', 'tag 2', 'tag 3']
        Spending.objects.create(
            date=datetime.today(),
            concept='Test 1',
            amount=10.30
        )

        Spending.objects.create(
            date=datetime.today() - timedelta(days=1),
            concept='Test 2',
            amount=12.30
        )

        Spending.objects.create(
            date=datetime.today() - timedelta(days=2),
            concept='Test 3',
            amount=1.98
        )
        self.spending_ids = [s.id for s in Spending.objects.all()]

    def test_add_tags_to_spend(self):
        form = {
            'tags': ','.join(self.tag_names),
            'spending_ids': ','.join(map(str, self.spending_ids))
        }

        self.client.post(
            '/gastos/add_tags/{}'.format(
                ','.join(map(str, self.spending_ids))
            ),
            data=form
        )

        # todos los gastos deberian tener todas las tags
        for spend in Spending.objects.all():
            tags = list(set(spend.tags.all()))
            self.assertEqual(len(tags), len(self.tag_names))

    def test_add_tags_to_spend_with_regex_all(self):
        form = {
            'regex': '^.*$'
        }

        response = self.client.post(
            '/gastos/add_tags_with_regex/{}'.format(self.spending_ids[1]),
            data=form
        )

        # en el contexto devuelto deberia venir la lista con
        # todos los ids de gastos
        self.assertEqual(
            response.context['spending_ids'],
            ','.join(map(str, self.spending_ids))
        )

    def test_add_tags_to_spend_with_regex_one(self):
        search_chars = '1'
        form = {
            'regex': '^.*{}.*$'.format(search_chars)
        }

        response = self.client.post(
            '/gastos/add_tags_with_regex/{}'.format(self.spending_ids[1]),
            data=form
        )

        # en el contexto devuelto deberian venir solo los buscados
        self.assertEqual(
            response.context['spending_ids'],
            str(
                Spending.objects.filter(
                    concept__contains=search_chars).count()
            )
        )
