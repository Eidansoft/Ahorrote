# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Spending(models.Model):
    date = models.DateField()
    concept = models.TextField()
    amount = models.DecimalField(max_digits=7, decimal_places=2)

    class Meta:
        unique_together = (('concept', 'amount', 'date'),)

    def __unicode__(self):
        return '{} ({})'.format(self.date, self.amount)

    def __str__(self):
        return '{} ({})'.format(self.date, self.amount)
