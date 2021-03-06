from django.urls import path
from .views import PollView, QuestionsView, UsersView, AnswersView

app_name = "polls"


urlpatterns = [
    path("polls/", PollView.as_view()),
    path("polls/<int:pk>", PollView.as_view()),
    path("questions/", QuestionsView.as_view()),
    path("questions/<int:q_pk>", QuestionsView.as_view()),
    path("polls/<int:p_pk>/questions/", QuestionsView.as_view()),
    path("auth/", UsersView.as_view()),
    path("answers/<int:u_pk>", AnswersView.as_view()),
    path("polls/<int:p_pk>/questions/<int:q_pk>", AnswersView.as_view()),
]
