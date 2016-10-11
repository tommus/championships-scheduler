import itertools
from string import ascii_uppercase

import random
from django.contrib.auth.models import User
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.viewsets import (
    GenericViewSet,
    ModelViewSet
)

from csa.championship.models import Championship, Group, Participation, Team, Match
from csa.championship.serializers import (
    ChampionshipSerializer,
    GroupSerializer,
    ParticipationSerializer,
    ResultsSerializer,
    TeamSerializer,
    MatchSerializer
)


class ChampionshipViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Championship.objects.all()
    serializer_class = ChampionshipSerializer


class ScheduleChampionshipViewSet(CreateModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Championship.objects.none()
    serializer_class = ChampionshipSerializer

    def create(self, request, *args, **kwargs):
        name = request.data.get('name')
        groups = request.data.get('groups')
        home_away = request.data.get('home_away')
        players = [player.get('id') for player in request.data.get('players')]
        teams = [team.get('id') for team in request.data.get('teams')]

        players = User.objects.filter(id__in=players)
        teams = Team.objects.filter(id__in=teams)

        # todo: validation

        championship = self._prepare_championship(name, groups, players, teams, home_away)
        self._prepare_participates(championship, players, teams)
        self._prepare_groups(championship, groups)
        self._prepare_matches(championship, home_away)

        return Response(status=HTTP_200_OK)

    def _prepare_championship(self, name, groups, players, teams, home_away):
        championship = Championship(
            name=name,
            groups=groups,
            home_and_away=home_away
        )
        championship.save()

        [championship.players.add(player) for player in players]
        [championship.teams.add(team) for team in teams]

        return championship

    def _prepare_participates(self, championship, players, teams):
        player_models = list(players)
        team_models = list(teams)

        player_teams_count = len(team_models) / len(player_models)
        player_teams_count = int(player_teams_count)

        for player in player_models:
            player_pick = random.sample(team_models, player_teams_count)

            team_models = [team for team in team_models if team not in player_pick]

            for team in player_pick:
                participation = Participation(
                    player=player,
                    team=team,
                    championship=championship
                )
                participation.save()

    def _prepare_groups(self, championship, groups):
        championship_participates = Participation.objects.filter(championship=championship)
        championship_players = User.objects.filter(championship=championship)

        players_per_group = len(championship_participates) / len(championship_players) / groups
        players_per_group = int(players_per_group)

        available_participates = list(championship_participates)

        for i in range(championship.groups):
            group_name = ascii_uppercase[i]
            group_participates = []

            group = Group(
                championship=championship,
                name=group_name,
            )
            group.save()

            for player in championship_players:
                available_player_teams = [p for p in available_participates if p.player.id == player.id]

                if len(available_player_teams) < players_per_group:
                    selected_player_teams = available_player_teams
                else:
                    selected_player_teams = random.sample(available_player_teams, players_per_group)

                [group_participates.append(t) for t in selected_player_teams]
                available_participates = [p for p in available_participates if p not in selected_player_teams]

            for participate in group_participates:
                group.participates.add(participate)

    def _prepare_matches(self, championship, home_away):
        groups = Group.objects.filter(championship=championship)

        for group in groups:
            group_participates = Participation.objects.filter(group=group)
            pairs = list(itertools.combinations(group_participates, 2))
            random.shuffle(pairs)

            self._prepare_pairs(group, pairs, True)

            if home_away:
                self._prepare_pairs(group, pairs, False)

    def _prepare_pairs(self, group, pairs, home=True):
        for pair in pairs:
            if pair[0].player != pair[1].player:
                match = Match(
                    group=group,
                    host_team=pair[0 if home else 1],
                    guest_team=pair[1 if home else 0]
                )
                match.save()


class GroupViewSet(ModelViewSet):
    filter_fields = ['championship']
    permission_classes = [IsAuthenticated]
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class ParticipationViewSet(ModelViewSet):
    filter_fields = ['id', 'championship']
    permission_classes = [IsAuthenticated]
    queryset = Participation.objects.all()
    serializer_class = ParticipationSerializer


class ResultsViewSet(ModelViewSet):
    filter_fields = ['id', 'championship']
    permission_classes = [IsAuthenticated]
    queryset = Participation.objects.all()
    serializer_class = ResultsSerializer


class TeamViewSet(ModelViewSet):
    filter_fields = ['championship']
    permission_classes = [IsAuthenticated]
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class MatchViewSet(ModelViewSet):
    filter_fields = ['group__championship']
    permission_classes = [IsAuthenticated]
    queryset = Match.objects.all()
    serializer_class = MatchSerializer
