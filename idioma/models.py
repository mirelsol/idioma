#!/usr/bin/python
#-*- encoding:utf-8 *-*

from django.db import models


class Language(models.Model):
    label = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return self.label


class Topic(models.Model):
    label = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.label

    class Meta:
        ordering = ['label']


class ExpressionGen(models.Model):
    added_on = models.DateField(auto_now_add=True)
    updated_on = models.DateField(auto_now=True)
    
    topic = models.ForeignKey(Topic, null=True, blank=True)
    
    from_language = models.ForeignKey(Language, related_name='from_language')
    from_expr = models.CharField(max_length=255, help_text="Use | to separate multiple expressions")
    from_comment = models.TextField(max_length=255, null=True, blank=True)

    to_language = models.ForeignKey(Language, related_name='to_language')
    to_expr = models.CharField(max_length=255, help_text="Use | to separate multiple expressions")
    to_comment = models.TextField(max_length=255, null=True, blank=True)
    
    tatoeba_id = models.IntegerField(null=True, blank=True)

    def __unicode__(self):
        return "%s [%s]" % (self.from_expr, self.to_expr)

    class Meta:
        verbose_name = 'Expression'
        unique_together = ("from_expr", "to_expr")