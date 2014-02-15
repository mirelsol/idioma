#!/usr/bin/python
#-*- encoding:utf-8 *-*

import random

from django.shortcuts import render
from idioma.models import ExpressionIta
from idioma.forms import InitPlayForm
from idioma.forms import QuestionForm

def index(request):
    """
    Main view
    """
    response_page = "idioma/index.html"
    page_title = "Idioma Home"
    if request.method == 'POST':
        init_play_form = InitPlayForm(request.POST)
        if init_play_form.is_valid():
            request.session['language'] = init_play_form.cleaned_data['language']
            request.session['current_question_nb'] = 1
            request.session['nb_of_points'] = 0
            form = QuestionForm()
            form.current_question_nb = request.session['current_question_nb']
            form.nb_of_points = 0
            __ask_question(form, request)
            response_page = "idioma/question.html"
        else:
            form = init_play_form
    else:
        form = InitPlayForm()

    return render(
        request,
        response_page,
        {
          'page_title': page_title,
          'form': form,
        }
    )

def question(request):
    """
    Ask / evaluate a question
    """
    page_title = "Question"
    form = QuestionForm(request.POST)
    if form.is_valid():
        __evaluate_answer(form.cleaned_data['user_answer'], form, request)
        form.previous_user_answer = form.cleaned_data['user_answer']
        
    else:
        __evaluate_answer('', form, request)
        form.previous_user_answer = ''        

    form.previous_question = request.session['current_question']
    form.previous_answer = request.session['current_answer']
    form.previous_answer_comment = request.session['current_answer_comment']
    __ask_question(form, request)

    return render(
        request,
        'idioma/question.html',
        {
          'page_title': page_title,
          'form': form,
        }
    )

def __evaluate_answer(answer, form, request):
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
    else:
        form.result_message = "Wrong answer !"
        form.result_message_style = "isWrongAnswer"

    score = (request.session['nb_of_points'] * 20) / (request.session['current_question_nb'])
    request.session['current_question_nb'] = request.session['current_question_nb'] + 1
    form.current_question_nb = request.session['current_question_nb']
    form.nb_of_points = request.session['nb_of_points']
    form.score = score # + " / 20"

def __ask_question(question_form, request):
    """
    Ask a question to the user
    @param question_form : a form reprensenting a question
    @param request : HTTP request
    """
    expr = __get_random_question(request.session['language'])
    question_form.question = expr.french_expression
    question_form.comment = expr.comment_french
    # TODO : this doesn't work
    #questionForm.userAnswer.clean("")
    request.session['current_question'] = question_form.question
    # Get answer
    request.session['current_answer'] = expr.foreign_expression
    request.session['current_answer_comment'] = expr.comment_foreign

def __get_random_question(language_filter):
    """
    Choose a random question
    @param language_filter : the language
    """
    if language_filter == 'IT':
        expr_list = ExpressionIta.objects.all()
    elif language_filter == 'DE':
        expr_list = ExpressionGer.objects.all()
    else:
        raise Exception("'%s' language currently NOT supported" % language_filter)
    # TODO : check that exprSet is not empty
    expr_nb = random.randint(0, expr_list.count() - 1)
    return expr_list[expr_nb]
