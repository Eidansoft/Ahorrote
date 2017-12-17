# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Spending(models.Model):
    date = models.DateField()
    concept = models.CharField(max_length=250)
    amount = models.IntegerField(default=0)

