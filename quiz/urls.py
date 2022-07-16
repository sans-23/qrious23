from django.urls import path, re_path
from . import views

app_name = 'quiz'

urlpatterns = [
    re_path(r'^records/(?P<slug>[\w-]+)/(?P<userid>\d+)/$', views.response_page, name='responses'),
    re_path(r'^question/(?P<slug>[\w-]+)/create/$', views.QuestionCreate.as_view(), name='question_create'),
    re_path(r'^(?P<slug>[\w-]+)/delete/$', views.QuizDelete.as_view(), name='quiz_delete'),
    path('question/<int:pk>/update/', views.QuestionUpdate.as_view(), name='question_update'),
    path('question/<int:pk>/delete/', views.QuestionDelete.as_view(), name='question_delete'),
    re_path(r'^exam/(?P<slug>[\w-]+)/$', views.exam_view, name='exam'),
    re_path(r'^qlist/(?P<slug>[\w-]+)/$', views.question_list, name='question_list'),
]