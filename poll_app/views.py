from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Poll
from .serializers import PollSerializer


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
