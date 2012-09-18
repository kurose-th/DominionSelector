# -*- coding: utf-8 -*-
from django.db import models


class Set(models.Model):
    setid = models.IntegerField()
    name = models.CharField(max_length=5)
    ename = models.CharField(max_length=20)
    defaulton = models.BooleanField()

    def __unicode__(self):
        return self.name


class Card(models.Model):
    cardid = models.IntegerField()
    name = models.CharField(max_length=10)
    set = models.ForeignKey(Set)
    cost = models.IntegerField()
    potion = models.IntegerField()
    text = models.CharField(max_length=500)
    ename = models.CharField(max_length=30)
    vp = models.IntegerField()
    action = models.IntegerField()
    coin = models.IntegerField()
    draw = models.IntegerField()
    buy = models.IntegerField()
    attack = models.BooleanField()
    reaction = models.BooleanField()

    def __unicode__(self):
        return self.name
    
    
    