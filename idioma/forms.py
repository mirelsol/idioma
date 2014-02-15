#!/usr/bin/python
#-*- encoding:utf-8 *-*

from django import forms

class InitPlayForm(forms.Form):
    LANGUAGE_CHOICES = (
        ('IT', 'IT'),
        ('EN', 'EN'),
        ('DE', 'DE'),
    )
    language = forms.ChoiceField(label='Language',choices=LANGUAGE_CHOICES)


class QuestionForm(forms.Form):
    question = ""
    comment = ""
    current_question_nb = 0
    nb_of_points = 0
    nb_of_expr_left = 0
    score = ""
    result_message = ""
    result_message_style = ""
    previous_question = ""
    previous_answer = ""
    previous_user_answer = ""
    previous_answer_comment = ""
    #userAnswer = forms.CharField(label='Answer', initial="", attrs={'autocomplete':'off'})
    user_answer = forms.CharField(initial="", widget=forms.TextInput(attrs={'autocomplete':'off'}))

