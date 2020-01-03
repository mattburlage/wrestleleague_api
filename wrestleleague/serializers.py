from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework_jwt.settings import api_settings
from django.contrib.auth.models import User

from wrestleleague.models import Season, Event, MatchQuestion, Answer, Vote


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username',)


class UserSerializerWithToken(serializers.ModelSerializer):

    token = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True)

    def get_token(self, obj):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(obj)
        token = jwt_encode_handler(payload)
        return token

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    class Meta:
        model = User
        fields = ('token', 'username', 'password')


class SeasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Season
        fields = ('name', 'published')


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'


class MatchQuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)

    class Meta:
        model = MatchQuestion
        fields = [
            'question', 'image_url', 'correct_answer', 'event', 'text_answer',
            'points', 'answers'
        ]


class EventSerializer(serializers.ModelSerializer):
    match_questions = MatchQuestionSerializer(many=True)

    class Meta:
        model = Event
        fields = [
            'title', 'published', 'datetime', 'vote_open', 'vote_closed',
            'season', 'promotion', 'open_for', 'match_questions',
        ]


class VoteSerializer(serializers.ModelSerializer):
    points_awarded = serializers.FloatField(read_only=True)
    is_correct = serializers.BooleanField(read_only=True)
    added_on = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Vote
        fields = [
            'question', 'answer', 'text_answer', 'rationale',
            'points_awarded', 'is_correct', 'user', 'added_on'
        ]
