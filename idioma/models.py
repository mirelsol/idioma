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

    topics = models.ManyToManyField(Topic, related_name='topics')
    
    from_language = models.ForeignKey(Language, related_name='from_language')
    from_expr = models.CharField(max_length=255, help_text="Use | to separate multiple expressions")
    from_comment = models.TextField(max_length=255, null=True, blank=True)

    to_language = models.ForeignKey(Language, related_name='to_language')
    to_expr = models.CharField(max_length=255, help_text="Use | to separate multiple expressions")
    to_comment = models.TextField(max_length=255, null=True, blank=True)
    
    tatoeba_id = models.IntegerField(null=True, blank=True)

    def get_topics_labels(self):
        return [e['label'] for e in self.topics.values()]

    def __str__(self):
        return "%s [%s]" % (self.from_expr, self.to_expr)

    class Meta:
        verbose_name = 'Expression'
        unique_together = ("from_expr", "to_expr")