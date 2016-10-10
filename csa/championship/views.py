from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from csa.championship.models import Championship, Group, Participation, Team, Match
from csa.championship.serializers import (
    ChampionshipSerializer,
    GroupSerializer,
    ParticipationSerializer,
    ParticipateResultsSerializer,
    TeamSerializer,
    MatchSerializer
)


class ChampionshipViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Championship.objects.all()
    serializer_class = ChampionshipSerializer


class ChampionshipParticipatesViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Participation.objects.none()
    serializer_class = ParticipateResultsSerializer

    def get_queryset(self):
        id = self.kwargs.get('id')
        queryset = Participation.objects.filter(championship__id=id)
        return queryset


class GroupViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class ParticipationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Participation.objects.all()
    serializer_class = ParticipationSerializer


class ParticipateResultsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Participation.objects.none()
    serializer_class = ParticipateResultsSerializer


class TeamViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

    # def get_queryset(self):
    #     queryset = Team.objects.filter(
    #         participation__player=self.request.user
    #     )
    #
    #     return queryset

class MatchViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Match.objects.all()
    serializer_class = MatchSerializer
