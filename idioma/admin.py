#!/usr/bin/python
#-*- encoding:utf-8 *-*

from django.contrib import admin
from idioma.models import ExpressionGen, Language, Topic


class ExpressionAdmin(admin.ModelAdmin):
    list_display = ('french_expression', 'foreign_expression', 'tatoeba_id', 'added_on', 'updated_on')
    search_fields = ['french_expression', 'foreign_expression']

class ExpressionGenAdmin(admin.ModelAdmin):
    list_display = ('from_expr', 'to_expr', 'tatoeba_id', 'added_on', 'updated_on')
    list_filter = ('from_language', 'to_language')
    search_fields = ['from_expr', 'to_expr']


admin.site.register(ExpressionGen, ExpressionGenAdmin)
admin.site.register(Language)
admin.site.register(Topic)