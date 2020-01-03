from django.urls import path
from .views import current_user, UserList, SeasonsView, EventView, MatchQuestionView, VoteView

urlpatterns = [
    path('current_user/', current_user),
    path('users/', UserList.as_view()),
    path('seasons/', SeasonsView.as_view()),
    path('events/<int:season_id>', EventView.as_view()),
    path('questions/<int:eventid>', MatchQuestionView.as_view()),
    path('votes/', VoteView.as_view()),
]
