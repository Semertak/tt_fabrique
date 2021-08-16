from django.urls import path
from .views import PollView


app_name = "polls"


urlpatterns = [
    path("polls/", PollView.as_view()),
    path("polls/<int:pk>", PollView.as_view()),
]
