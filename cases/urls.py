from django.urls import path
from . import views

urlpatterns = [

    # Home
    path(
        '',
        views.home,
        name='home'
    ),

    # Player setup
    path(
        'play/',
        views.player,
        name='player'
    ),

    # Dashboard
    path(
        'dashboard/',
        views.dashboard,
        name='dashboard'
    ),

    # My Progress
    path(
        'progress/',
        views.progress,
        name='progress'
    ),

    # Case list
    path(
        'mystery/',
        views.mystery,
        name='mystery'
    ),

    # Case details
    path(
        'case/<int:case_id>/',
        views.case_detail,
        name='case_detail'
    ),

    # Questions
    path(
        'question/<int:case_id>/<int:question_number>/',
        views.question,
        name='question'
    ),

    # Result
    path(
        'result/',
        views.result,
        name='result'
    ),
]
