# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.conf import settings


# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=settings.MODEL_TAG_NAME_MAX_LEN)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class AutoTag(models.Model):
    name = models.CharField(max_length=50)
    expression = models.CharField(max_length=100)
    tags = models.ManyToManyField(Tag)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class Spending(models.Model):
    date = models.DateField()
    concept = models.TextField()
    amount = models.DecimalField(max_digits=7, decimal_places=2)
    tags = models.ManyToManyField(Tag, blank=True)

    class Meta:
        unique_together = (('concept', 'amount', 'date'),)

    def __unicode__(self):
        return '{} {} ({})'.format(self.date, self.concept[:20], self.amount)

    def __str__(self):
        return '{} {} ({})'.format(self.date, self.concept[:20], self.amount)
