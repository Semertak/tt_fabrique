from django.core.exceptions import ValidationError
from rest_framework import serializers

from .models import Poll, Question


class PollSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=25)
    description = serializers.CharField()
    start_date = serializers.DateField()
    end_date = serializers.DateField()

    def create(self, validated_data):
        return Poll.objects.create(**validated_data)

    def update(self, instance, validated_data):
        #TODO Скорее всего это можно сложить в какой-нибудь переопределенный is_valid()
        if validated_data.get('start_date') is not None:
            raise ValidationError("StartDate is not editable")

        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.end_date = validated_data.get('end_date', instance.end_date)
        instance.save()

        return instance

    class Meta:
        model = Poll
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    text = serializers.CharField()
    answer_type = serializers.IntegerField()
    answer_list = serializers.CharField()
    right_answer = serializers.CharField()

    class Meta:
        model = Question
        fields = '__all__'
