import itertools
from string import ascii_uppercase

import random
from django.contrib.admin import (
    ModelAdmin,
    register
)
from django.db.models import F, IntegerField, Q, Sum
from django.db.models.functions import Coalesce

from csa.championship.models import (
    Participation,
    Championship,
    Group,
    Match
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
    list_filter = ['player__username', 'group']

    def games_played(self, obj):
        home_played = Match.objects.filter(Q(first_team__id=obj.id) & Q(first_team_goals__isnull=False))
        away_played = Match.objects.filter(Q(second_team__id=obj.id) & Q(second_team_goals__isnull=False))
        return home_played.count() + away_played.count()

    def games_won(self, obj):
        home_won = Match.objects.filter(Q(first_team__id=obj.id) & Q(first_team_goals__gt=F('second_team_goals')))
        away_won = Match.objects.filter(Q(second_team__id=obj.id) & Q(second_team_goals__gt=F('first_team_goals')))
        return home_won.count() + away_won.count()

    def games_drawn(self, obj):
        home_drawn = Match.objects.filter(Q(first_team__id=obj.id) & Q(first_team_goals=F('second_team_goals')))
        away_drawn = Match.objects.filter(Q(second_team__id=obj.id) & Q(second_team_goals=F('first_team_goals')))
        return home_drawn.count() + away_drawn.count()

    def games_lost(self, obj):
        home_lost = Match.objects.filter(Q(first_team__id=obj.id) & Q(first_team_goals__lt=F('second_team_goals')))
        away_lost = Match.objects.filter(Q(second_team__id=obj.id) & Q(second_team_goals__lt=F('first_team_goals')))
        return home_lost.count() + away_lost.count()

    def goals_scored(self, obj):
        home_played = Match.objects.filter(Q(first_team__id=obj.id))
        away_played = Match.objects.filter(Q(second_team__id=obj.id))
        home_scored = home_played.aggregate(goals=Coalesce(Sum('first_team_goals', output_field=IntegerField()), 0))
        away_scored = away_played.aggregate(goals=Coalesce(Sum('second_team_goals', output_field=IntegerField()), 0))
        return home_scored['goals'] + away_scored['goals']

    def goals_lost(self, obj):
        home_played = Match.objects.filter(Q(first_team__id=obj.id))
        away_played = Match.objects.filter(Q(second_team__id=obj.id))
        home_lost = home_played.aggregate(goals=Coalesce(Sum('second_team_goals', output_field=IntegerField()), 0))
        away_lost = away_played.aggregate(goals=Coalesce(Sum('first_team_goals', output_field=IntegerField()), 0))
        return home_lost['goals'] + away_lost['goals']

    def points(self, obj):
        games_won = self.games_won(obj)
        games_drawn = self.games_drawn(obj)
        return games_won * 3 + games_drawn


@register(Championship)
class ChampionshipAdmin(ModelAdmin):
    def save_model(self, request, obj, form, change):
        championship = form.save(commit=True)

        self._prepare_groups(championship)
        self._prepare_matches(championship)

    def _prepare_groups(self, championship):
        championship_participates = Participation.objects.filter(championship__name=championship.name)
        human_players = list(set([participate.player for participate in championship_participates]))

        available_participates = list(championship_participates)

        for i in range(championship.groups):
            group_name = ascii_uppercase[i]
            group_participates = []

            group = Group(
                championship=championship,
                name=group_name,
            )
            group.save()

            for player in human_players:
                available_player_teams = [p for p in available_participates if p.player.id == player.id]

                if len(available_player_teams) < championship.players_per_group:
                    selected_player_teams = available_player_teams
                else:
                    selected_player_teams = random.sample(available_player_teams, championship.players_per_group)

                [group_participates.append(t) for t in selected_player_teams]
                available_participates = [p for p in available_participates if p not in selected_player_teams]

            for participate in group_participates:
                group.participates.add(participate)

    def _prepare_matches(self, championship):
        groups = Group.objects.filter(championship__name=championship.name)

        for group in groups:
            group_participates = Participation.objects.filter(group=group)
            pairs = list(itertools.combinations(group_participates, 2))
            random.shuffle(pairs)

            for pair in pairs:
                if pair[0].player != pair[1].player:
                    match = Match(
                        group=group,
                        first_team=pair[0],
                        second_team=pair[1]
                    )
                    match.save()

            if championship.home_and_away:
                for pair in pairs:
                    if pair[0].player != pair[1].player:
                        match = Match(
                            championship=championship,
                            first_team=pair[1],
                            second_team=pair[0]
                        )
                        match.save()


@register(Match)
class MatchAdmin(ModelAdmin):
    list_filter = ['group__championship__name', 'group__name']
    list_display = ['first_team', 'first_team_goals', 'second_team_goals', 'second_team']
    list_display_links = list_display


@register(Group)
class GroupAdmin(ModelAdmin):
    list_filter = ['championship__name']
