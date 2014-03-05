#!/usr/bin/python
#-*- encoding:utf-8 *-*

from django import forms
from idioma.models import Language, Topic

languages = Language.objects.all()

class InitPlayForm(forms.Form):
    question_language = forms.ChoiceField(label='Question language', choices=((l.id, l.label) for l in languages))
    response_language = forms.ChoiceField(label='Response language', choices=((l.id, l.label) for l in languages))

    def clean(self):
        cleaned_data = super(InitPlayForm, self).clean()
        lang_from = cleaned_data['question_language']
        lang_to = cleaned_data['response_language']
        if lang_from == lang_to:
            raise forms.ValidationError("Question and response languages can't be identical")
        return cleaned_data


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

