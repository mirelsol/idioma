#!/usr/bin/python
#-*- encoding:utf-8 *-*

from django.db import models

class Expression(models.Model):
    added_on = models.DateField(auto_now_add=True)
    updated_on = models.DateField(auto_now=True)
    foreign_expression = models.CharField(max_length=255, help_text="Use | to separate multiple expressions")
    french_expression = models.CharField(max_length=255)
    comment_foreign = models.TextField(max_length=255, null=True, blank=True)
    comment_french = models.TextField(max_length=255, null=True, blank=True)
    tatoeba_id = models.IntegerField(null=True, blank=True)

    def __unicode__(self):
        return "%s [%s]" % (self.foreign_expression, self.french_expression)

class ExpressionIta(Expression):
    class Meta:
        verbose_name = "Expression italienne"
        verbose_name_plural = "Expressions italiennes"

class ExpressionGer(Expression):
    class Meta:
        verbose_name = "Expression allemande"
        verbose_name_plural = "Expressions allemandes"
