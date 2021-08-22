from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, get_list_or_404
from django.utils import timezone

from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Poll, Question, Users
from .serializers import PollSerializer, QuestionSerializer, UsersSerializer


class PollView(APIView):
    def get(self, request):
        token = request.headers.get('Handmade-Token', '')
        if Users.objects.filter(token=token):
            polls = Poll.objects.all()
        else:
            today = timezone.now().date()
            polls = Poll.objects.filter(start_date__lte=today, end_date__gte=today)

        serialized_data = PollSerializer(polls, many=True).data
        return Response({"Polls": serialized_data})

    def post(self, request):
        poll = request.data.get('poll')
        serializer = PollSerializer(data=poll)
        if serializer.is_valid(raise_exception=True):
            saved_poll = serializer.save()
            return Response({"success": f'New poll Id: {saved_poll.id}, Title: {saved_poll.title}'})

    def put(self, request, pk):
        old_poll = get_object_or_404(Poll.objects.all(), pk=pk)
        new_data = request.data.get('poll')
        serializer = PollSerializer(instance=old_poll, data=new_data, partial=True)
        if serializer.is_valid(raise_exception=True):
            saved_poll = serializer.save()
            return Response({"success": "Poll '{}' updated successfully".format(saved_poll.title)})

    def delete(self, request, pk):
        poll = get_object_or_404(Poll.objects.all(), pk=pk)
        poll.delete()
        return Response({"message": "Poll with id `{}` has been deleted.".format(pk)}, status=204)


class QuestionsView(APIView):
    def get(self, request, p_pk):
        questions = get_list_or_404(Question, poll_id=p_pk)
        serialized_data = QuestionSerializer(questions, many=True).data
        return Response({"Questions": serialized_data})

    def post(self, request):
        questions = request.data.get('questions')
        serializer = QuestionSerializer(data=questions)
        if serializer.is_valid(raise_exception=True):
            saved_questions = serializer.save()
            return Response({"success": f'New question Id: {saved_questions.id}, for poll number: {saved_questions.poll_id}'})

    def put(self, request, q_pk):
        old_question = get_object_or_404(Question.objects.all(), pk=q_pk)
        new_data = request.data.get('question')
        serializer = QuestionSerializer(instance=old_question, data=new_data, partial=True)
        if serializer.is_valid(raise_exception=True):
            saved_questions = serializer.save()
            return Response({"success": "Question '{}' updated successfully".format(saved_questions.id)})

    def delete(self, request, q_pk):
        question = get_object_or_404(Question.objects.all(), pk=q_pk)
        question.delete()
        return Response({"message": "Question with id `{}` has been deleted.".format(q_pk)}, status=204)


class UsersView(APIView):
    def post(self, request):
        user = request.data.get('user', {})
        if user:
            try:
                user_from_db = Users.objects.get(
                    login=user.get('login'),
                    password=user.get('password')
                )
                return Response({"token": user_from_db.token})
            except ObjectDoesNotExist:
                return Response({
                    "error": {
                        "code": 691,
                        "message": "Incorrect Login or Password"
                    }
                })
        else:
            serializer = UsersSerializer(data={'login': '', 'password': ''})
            if serializer.is_valid(raise_exception=True):
                saved_user = serializer.save()
                return Response({"ID": saved_user.id})

