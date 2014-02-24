from django.conf.urls import patterns, url

from idioma import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'), # ex: /idioma/
    url(r'^question/$', views.question, name='question'), # ex: /idioma/question
    url(r'^terminate/$', views.terminate, name='terminate'),
)
