from django.shortcuts import render

from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from rest_framework import permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from wrestleleague.models import Season, Event, MatchQuestion, Vote
from .serializers import UserSerializer, UserSerializerWithToken, SeasonSerializer, EventSerializer, \
    MatchQuestionSerializer, VoteSerializer


@api_view(['GET'])
def current_user(request):
    """
    Determine the current user by their token, and return their data
    """

    serializer = UserSerializer(request.user)
    return Response(serializer.data)


class UserList(APIView):
    """
    Create a new user. It's called 'UserList' because normally we'd have a get
    method here too, for retrieving a list of all User objects.
    """

    permission_classes = (permissions.AllowAny,)

    def post(self, request, fmt=None):
        serializer = UserSerializerWithToken(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SeasonsView(APIView):

    def get(self, request):
        seasons = Season.objects.filter(published=True)
        serializer = SeasonSerializer(seasons, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class EventView(APIView):

    def get(self, request, season_id=None):
        events = Event.objects.filter(published=True)
        if season_id:
            events = events.filter(season_id=season_id)

        serializer = EventSerializer(events, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class MatchQuestionView(APIView):
    def get(self, request, eventid):
        questions = MatchQuestion.objects.filter(event_id=eventid)

        serializer = MatchQuestionSerializer(questions, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class VoteView(APIView):
    def get(self, request):
        votes = Vote.objects.filter(user=request.user)

        serializer = VoteSerializer(votes, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data['votes']
        for item in data:
            item['user'] = request.user.id

        serializer = VoteSerializer(data=data, many=True)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
