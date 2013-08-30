from django.conf.urls import patterns, url

from idioma import views

urlpatterns = patterns('',
    # ex: /idioma/
    url(r'^$', views.index, name='index'),
    #url(r'^/question/$', views.question, name='question'),
    # ex: /idioma/question
    url(r'^question/$', views.question, name='question'),
)
