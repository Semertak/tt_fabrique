from django.shortcuts import get_object_or_404, get_list_or_404

from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Poll, Question
from .serializers import PollSerializer, QuestionSerializer


class PollView(APIView):
    def get(self, request):
        polls = Poll.objects.all()
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

    def post(self, request, p_pk):
        questions = request.data.get('questions')
        serializer = QuestionSerializer(data=questions)
        if serializer.is_valid(raise_exception=True):
            saved_questions = serializer.save()
            return Response({"success": f'New poll Id: {saved_questions.id}, for poll number: {saved_questions.poll_id}'})

    def put(self, request, p_pk, q_pk):
        old_question = get_object_or_404(Question.objects.all(), pk=q_pk)
        new_data = request.data.get('question')
        serializer = QuestionSerializer(instance=old_question, data=new_data, partial=True)
        if serializer.is_valid(raise_exception=True):
            saved_questions = serializer.save()
            return Response({"success": "Question '{}' updated successfully".format(saved_questions.id)})

    def delete(self, request, p_pk, q_pk):
        question = get_object_or_404(Question.objects.all(), pk=q_pk)
        question.delete()
        return Response({"message": "Question with id `{}` has been deleted.".format(q_pk)}, status=204)
