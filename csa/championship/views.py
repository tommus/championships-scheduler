from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from csa.championship.models import Championship, Group, Participation, Team, Match
from csa.championship.serializers import ChampionshipSerializer, GroupSerializer, ParticipationSerializer, \
    TeamSerializer, MatchSerializer


class ChampionshipViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    queryset = Championship.objects.all()
    serializer_class = ChampionshipSerializer


class GroupViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class ParticipationViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    queryset = Participation.objects.all()
    serializer_class = ParticipationSerializer


class TeamViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class MatchViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    queryset = Match.objects.all()
    serializer_class = MatchSerializer
