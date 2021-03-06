import enum

from django.db import models
from django.core.exceptions import ValidationError


# Answer Types
class AnswerTypes(enum.Enum):
    single = 0
    multiply = 1
    text = 2


# Poll model
class Poll(models.Model):
    title = models.CharField(max_length=25)
    description = models.TextField(null=True)
    start_date = models.DateField()
    end_date = models.DateField()

    def clean(self):
        super().clean()
        if self.start_date > self.end_date:
            raise ValidationError("EndDate less then StartDate")


# Question model
class Question(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    text = models.TextField()
    answer_type = models.IntegerField(default=AnswerTypes.single)
    answer_list = models.TextField()
    right_answer = models.TextField()


# Users
class Users(models.Model):
    login = models.TextField(blank=True)
    password = models.TextField(blank=True)
    token = models.TextField(blank=True)


# Answers
class Answers(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.TextField()
