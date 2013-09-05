#!/usr/bin/python
#-*- encoding:utf-8 *-*

from django.contrib import admin
from idioma.models import ExpressionIta, ExpressionGer


class ExpressionAdmin(admin.ModelAdmin):
    list_display = ('french_expression', 'foreign_expression', 'tatoeba_id', 'added_on', 'updated_on')
    search_fields = ['french_expression', 'foreign_expression']


admin.site.register(ExpressionIta, ExpressionAdmin)
admin.site.register(ExpressionGer, ExpressionAdmin)
