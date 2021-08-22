from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, get_list_or_404
from django.utils import timezone
from rest_framework.exceptions import PermissionDenied

from rest_framework.response import Response
from rest_framework.views import APIView

from .access_control import is_request_by_admin
from .models import Poll, Question, Users, Answers
from .serializers import PollSerializer, QuestionSerializer, UsersSerializer, AnswersSerializer


class PollView(APIView):
    def get(self, request):
        if is_request_by_admin(request):
            polls = Poll.objects.all()
        else:
            today = timezone.now().date()
            polls = Poll.objects.filter(start_date__lte=today, end_date__gte=today)

        serialized_data = PollSerializer(polls, many=True).data
        return Response({"Polls": serialized_data})

    def post(self, request):
        if not is_request_by_admin(request):
            raise PermissionDenied()

        poll = request.data.get('poll')
        serializer = PollSerializer(data=poll)
        if serializer.is_valid(raise_exception=True):
            saved_poll = serializer.save()
            return Response({"success": f'New poll Id: {saved_poll.id}, Title: {saved_poll.title}'})

    def put(self, request, pk):
        if not is_request_by_admin(request):
            raise PermissionDenied()

        old_poll = get_object_or_404(Poll.objects.all(), pk=pk)
        new_data = request.data.get('poll')
        serializer = PollSerializer(instance=old_poll, data=new_data, partial=True)
        if serializer.is_valid(raise_exception=True):
            saved_poll = serializer.save()
            return Response({"success": "Poll '{}' updated successfully".format(saved_poll.title)})

    def delete(self, request, pk):
        if not is_request_by_admin(request):
            raise PermissionDenied()

        poll = get_object_or_404(Poll.objects.all(), pk=pk)
        poll.delete()
        return Response({"message": "Poll with id `{}` has been deleted.".format(pk)}, status=204)


class QuestionsView(APIView):
    def get(self, request, p_pk):
        # todo Отсутствие вопросов в опросе не должно падать с 404
        questions = get_list_or_404(Question, poll_id=p_pk)
        serialized_data = QuestionSerializer(questions, many=True).data

        # Не показывать обычным пользователям правильный ответ
        if not is_request_by_admin(request):
            for rec in serialized_data:
                del rec['right_answer']

        return Response({"Questions": serialized_data})

    def post(self, request):
        if not is_request_by_admin(request):
            raise PermissionDenied()

        questions = request.data.get('questions')
        serializer = QuestionSerializer(data=questions)
        if serializer.is_valid(raise_exception=True):
            saved_questions = serializer.save()
            return Response({"success": f'New question Id: {saved_questions.id}, for poll number: {saved_questions.poll_id}'})

    def put(self, request, q_pk):
        if not is_request_by_admin(request):
            raise PermissionDenied()

        old_question = get_object_or_404(Question.objects.all(), pk=q_pk)
        new_data = request.data.get('question')
        serializer = QuestionSerializer(instance=old_question, data=new_data, partial=True)
        if serializer.is_valid(raise_exception=True):
            saved_questions = serializer.save()
            return Response({"success": "Question '{}' updated successfully".format(saved_questions.id)})

    def delete(self, request, q_pk):
        if not is_request_by_admin(request):
            raise PermissionDenied()

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
                return Response({"USER_ID": saved_user.id})


class AnswersView(APIView):
    def get(self, request, u_pk):
        answers = get_list_or_404(Answers, user_id=u_pk)
        serialized_data = AnswersSerializer(answers, many=True).data
        for rec in serialized_data:
            rec['poll'] = Question.objects.get(id=rec['question']).poll.id
            rec['question_text'] = Question.objects.get(id=rec['question']).text
        return Response({"Questions": serialized_data})

    def post(self, request, p_pk, q_pk):
        answer = request.data.get('answer')
        user_id = request.headers.get('User-Id', None)
        answer['question'] = q_pk
        answer['user'] = user_id
        serializer = AnswersSerializer(data=answer)
        if serializer.is_valid(raise_exception=True):
            saved_answer = serializer.save()
            return Response({"success": f'New answer Id: {saved_answer.id}, for question number: {saved_answer.question_id}'})
