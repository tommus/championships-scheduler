import itertools
from string import ascii_uppercase

import random
from django.contrib.admin import (
    ModelAdmin,
    register
)
from django.contrib.auth.models import User
from django.db.models import Count, F, IntegerField, Q, Sum
from django.db.models.functions import Coalesce
from django.forms import (
    ModelForm,
    BooleanField
)

from csa.championship.models import (
    Participation,
    Championship,
    Group,
    Match,
    Team
)


@register(Participation)
class ParticipationAdmin(ModelAdmin):
    list_display = [
        'team',
        'player',
        'games_played',
        'games_won',
        'games_drawn',
        'games_lost',
        'goals_scored',
        'goals_lost',
        'points'
    ]
    list_display_links = ['team']
    list_filter = ['player__username', 'group', 'championship']

    def get_queryset(self, request):
        queryset = super(ParticipationAdmin, self).get_queryset(request)
        queryset = queryset.annotate(Count('championship'))
        return queryset

    def games_played(self, obj):
        home_played = Match.objects.filter(Q(host_team=obj) & Q(host_team_goals__isnull=False))
        away_played = Match.objects.filter(Q(guest_team=obj) & Q(guest_team_goals__isnull=False))
        return home_played.count() + away_played.count()

    def games_won(self, obj):
        home_won = Match.objects.filter(Q(host_team=obj) & Q(host_team_goals__gt=F('guest_team_goals')))
        away_won = Match.objects.filter(Q(guest_team=obj) & Q(guest_team_goals__gt=F('host_team_goals')))
        return home_won.count() + away_won.count()

    def games_drawn(self, obj):
        home_drawn = Match.objects.filter(Q(host_team=obj) & Q(host_team_goals=F('guest_team_goals')))
        away_drawn = Match.objects.filter(Q(guest_team=obj) & Q(guest_team_goals=F('host_team_goals')))
        return home_drawn.count() + away_drawn.count()

    def games_lost(self, obj):
        home_lost = Match.objects.filter(Q(host_team=obj) & Q(host_team_goals__lt=F('guest_team_goals')))
        away_lost = Match.objects.filter(Q(guest_team=obj) & Q(guest_team_goals__lt=F('host_team_goals')))
        return home_lost.count() + away_lost.count()

    def goals_scored(self, obj):
        home_played = Match.objects.filter(Q(host_team=obj))
        away_played = Match.objects.filter(Q(guest_team=obj))
        home_scored = home_played.aggregate(goals=Coalesce(Sum('host_team_goals', output_field=IntegerField()), 0))
        away_scored = away_played.aggregate(goals=Coalesce(Sum('guest_team_goals', output_field=IntegerField()), 0))
        return home_scored['goals'] + away_scored['goals']

    def goals_lost(self, obj):
        home_played = Match.objects.filter(Q(host_team=obj))
        away_played = Match.objects.filter(Q(guest_team=obj))
        home_lost = home_played.aggregate(goals=Coalesce(Sum('guest_team_goals', output_field=IntegerField()), 0))
        away_lost = away_played.aggregate(goals=Coalesce(Sum('host_team_goals', output_field=IntegerField()), 0))
        return home_lost['goals'] + away_lost['goals']

    def points(self, obj):
        games_won = self.games_won(obj)
        games_drawn = self.games_drawn(obj)
        return games_won * 3 + games_drawn


class ChampionshipForm(ModelForm):
    generate_schedule = BooleanField(required=False, initial=True)

    class Meta:
        fields = '__all__'
        model = Championship


@register(Championship)
class ChampionshipAdmin(ModelAdmin):
    fields = ['name', 'groups', 'players', 'teams', 'home_and_away', 'generate_schedule']
    form = ChampionshipForm

    def save_model(self, request, obj, form, change):
        championship = form.save(commit=True)

        self._prepare_participates(championship)

        if form.data.get('generate_schedule'):
            self._prepare_groups(championship)
            self._prepare_matches(championship)

    def _prepare_participates(self, championship):
        teams = list(Team.objects.filter(championship=championship))
        players = list(User.objects.filter(championship=championship))

        player_teams_count = len(teams) / len(players)
        player_teams_count = int(player_teams_count)
        print(player_teams_count)

        for player in players:
            player_pick = random.sample(teams, player_teams_count)

            teams = [team for team in teams if team not in player_pick]

            for team in player_pick:
                participation = Participation(
                    player=player,
                    team=team,
                    championship=championship
                )
                participation.save()

    def _prepare_groups(self, championship):
        championship_participates = Participation.objects.filter(championship=championship)
        championship_players = User.objects.filter(championship=championship)

        players_per_group = len(championship_participates) / len(championship_players) / championship.groups
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

    def _prepare_matches(self, championship):
        groups = Group.objects.filter(championship=championship)

        for group in groups:
            group_participates = Participation.objects.filter(group=group)
            pairs = list(itertools.combinations(group_participates, 2))
            random.shuffle(pairs)

            self._prepare_pairs(group, pairs, True)

            if championship.home_and_away:
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


@register(Match)
class MatchAdmin(ModelAdmin):
    list_filter = ['group__championship__name', 'group__name']
    list_display = ['host_team', 'host_team_goals', 'guest_team_goals', 'guest_team']
    list_display_links = list_display


@register(Group)
class GroupAdmin(ModelAdmin):
    list_filter = ['championship__name']


@register(Team)
class TeamAdmin(ModelAdmin):
    pass
