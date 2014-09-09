#!/usr/bin/python
#-*- encoding:utf-8 *-*

from django.contrib import admin
from django.forms import CheckboxSelectMultiple
from django.db import models
from idioma.models import ExpressionGen, Language, Topic


class ExpressionGenAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }

    list_display = ('from_expr', 'to_expr', 'get_str_topics_labels', 'tatoeba_id', 'added_on', 'updated_on')
    list_filter = ('from_language', 'to_language')
    search_fields = ['from_expr', 'to_expr']

    def get_str_topics_labels(self, obj):
        return ", ".join(obj.get_topics_labels())

admin.site.register(ExpressionGen, ExpressionGenAdmin)
admin.site.register(Language)
admin.site.register(Topic)