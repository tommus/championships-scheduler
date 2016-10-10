from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from csa.championship.models import Championship, Group, Participation, Team, Match
from csa.championship.serializers import (
    ChampionshipSerializer,
    GroupSerializer,
    ParticipationSerializer,
    ParticipateResultsSerializer,
    TeamSerializer,
    MatchSerializer
)


class ChampionshipViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Championship.objects.all()
    serializer_class = ChampionshipSerializer


class ChampionshipParticipatesViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Participation.objects.none()
    serializer_class = ParticipateResultsSerializer

    def get_queryset(self):
        id = self.kwargs.get('id')
        queryset = Participation.objects.filter(championship__id=id)
        return queryset


class GroupViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class ParticipationViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Participation.objects.all()
    serializer_class = ParticipationSerializer


class ParticipateResultsViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Participation.objects.none()
    serializer_class = ParticipateResultsSerializer


class TeamViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class MatchViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Match.objects.all()
    serializer_class = MatchSerializer
