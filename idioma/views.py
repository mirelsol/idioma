#!/usr/bin/python
#-*- encoding:utf-8 *-*

import random

from django.shortcuts import render
from django.db.models import Q

from idioma.models import ExpressionGen, Language, Topic
from idioma.forms import InitPlayForm
from idioma.forms import QuestionForm

_expr_list = []
_cur_expr_index = 0
_wrong_answered_list = []

def index(request):
    """
    Main view
    """
    global _expr_list
    response_page = "idioma/index.html"
    page_title = "Idioma Home"
    if request.method == 'POST':
        init_play_form = InitPlayForm(request.POST)
        if init_play_form.is_valid():
            _wrong_answered_list = []
            question_lang_id = init_play_form.cleaned_data['question_language']
            response_lang_id = init_play_form.cleaned_data['response_language']
            topic_id = init_play_form.cleaned_data['topic']
            request.session['topic'] = u'Everything'
            if topic_id != '-1':
                request.session['topic'] = Topic.objects.get(id=topic_id).label
            
            _init_question_list(question_lang_id, response_lang_id, topic_id)

            request.session['question_language'] = Language.objects.get(id=question_lang_id).label
            request.session['response_language'] = Language.objects.get(id=response_lang_id).label

            
            request.session['current_question_nb'] = 1
            request.session['nb_of_points'] = 0
            form = QuestionForm()
            form.current_question_nb = request.session['current_question_nb']
            form.nb_of_points = 0
            _ask_question(form, request)
            response_page = "idioma/question.html"
        else:
            form = init_play_form
    else:
        form = InitPlayForm()
    request.session['plop'] = 'plop'
    return render(
        request,
        response_page,
        {
          'page_title': page_title,
          'form': form,
        }
    )

def terminate(request):
    page_title = "The end!"
    return render(
        request,
        'idioma/terminate.html',
        {
          'expr_list': _wrong_answered_list,
          'page_title': page_title,
        }
    )    

def question(request):
    """
    Ask / evaluate a question
    """
    if len(_expr_list) == 0:
        # No more questions in the list (=> only correct answers!) => start from the beginning
        _init_question_list(request.session['language'])
    page_title = "Question"
    form = QuestionForm(request.POST)
    if form.is_valid():
        _evaluate_answer(form.cleaned_data['user_answer'], form, request)
        form.previous_user_answer = form.cleaned_data['user_answer']
        
    else:
        _evaluate_answer('', form, request)
        form.previous_user_answer = ''        

    form.previous_question = request.session['current_question']
    form.previous_answer = request.session['current_answer']
    form.previous_answer_comment = request.session['current_answer_comment']
    _ask_question(form, request)

    return render(
        request,
        'idioma/question.html',
        {
          'page_title': page_title,
          'form': form,
        }
    )

def _evaluate_answer(answer, form, request):
    """
    Evaluate the user answer
    @param answer : answer given by the user
    @param form : current form
    @param request : HTTP request
    """
    # An answer can have multiple items separated by ' | '. This means that all items are right
    right_answer_list = request.session['current_answer'].lower().split(' | ')
    if answer is not None and answer != '' and answer.lower() in right_answer_list:
        request.session['nb_of_points'] = request.session['nb_of_points'] + 1
        form.result_message = "Correct answer !"
        form.result_message_style = "isCorrectAnswer"
        del _expr_list[_cur_expr_index]
    else:
        form.result_message = "Wrong answer !"
        form.result_message_style = "isWrongAnswer"
        _wrong_answered_list.append(" | ".join(right_answer_list))

    score = (request.session['nb_of_points'] * 20) / (request.session['current_question_nb'])
    request.session['current_question_nb'] = request.session['current_question_nb'] + 1
    form.current_question_nb = request.session['current_question_nb']
    form.nb_of_points = request.session['nb_of_points']
    form.score = score # + " / 20"

def _ask_question(question_form, request):
    """
    Ask a question to the user
    @param question_form : a form reprensenting a question
    @param request : HTTP request
    """
    expr = _get_random_question()
    question_form.question = expr.to_expr
    question_form.comment = expr.to_comment
    question_form.nb_of_expr_left = len(_expr_list)
    request.session['current_question'] = question_form.question
    # Get answer
    request.session['current_answer'] = expr.from_expr
    request.session['current_answer_comment'] = expr.from_comment

def _get_random_question():
    """
    Choose a random question
    """
    global _cur_expr_index
    _cur_expr_index = random.randint(0, len(_expr_list) - 1)
    return _expr_list[_cur_expr_index]

def _init_question_list(question_lang_id, response_lang_id, c_topic_id):
    global _expr_list
    expr_gen_qs = ExpressionGen.objects.filter(
                        Q(from_language_id=response_lang_id, to_language_id=question_lang_id) |
                        Q(from_language_id=question_lang_id, to_language_id=response_lang_id)
                )
    if c_topic_id != '-1':
        expr_gen_qs = expr_gen_qs.filter(topic_id = c_topic_id)
    _expr_list = list(expr_gen_qs)