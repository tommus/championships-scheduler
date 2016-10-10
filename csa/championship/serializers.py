from django.db.models import F, IntegerField, Q, Sum
from django.db.models.functions import Coalesce
from rest_framework import serializers

from csa.championship.models import Championship, Group, Participation, Team, Match


class ChampionshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Championship


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group


class ParticipationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participation


class ParticipateResultsSerializer(serializers.ModelSerializer):
    team = serializers.SerializerMethodField()
    player = serializers.SerializerMethodField()
    results = serializers.SerializerMethodField()

    class Meta:
        model = Participation

    def get_team(self, obj):
        return str(obj.team.name)

    def get_player(self, obj):
        return str(obj.player.username)

    def get_results(self, obj):
        games_won = self._get_games_won(obj)
        games_drawn = self._get_games_drawn(obj)
        games_lost = self._get_games_lost(obj)
        games_plaed = games_won + games_drawn + games_lost
        goals_scored = self._get_goals_scored(obj)
        goals_lost = self._get_goals_lost(obj)
        points = games_won * 3 + games_drawn

        return {
            'games_played': games_plaed,
            'games_won': games_won,
            'games_drawn': games_drawn,
            'games_lost': games_lost,
            'goals_scored': goals_scored,
            'goals_lost': goals_lost,
            'points': points
        }

    def _get_games_won(self, obj):
        home_won = Match.objects.filter(Q(first_team__id=obj.id) & Q(first_team_goals__gt=F('second_team_goals')))
        away_won = Match.objects.filter(Q(second_team__id=obj.id) & Q(second_team_goals__gt=F('first_team_goals')))
        return home_won.count() + away_won.count()

    def _get_games_drawn(self, obj):
        home_drawn = Match.objects.filter(Q(first_team__id=obj.id) & Q(first_team_goals=F('second_team_goals')))
        away_drawn = Match.objects.filter(Q(second_team__id=obj.id) & Q(second_team_goals=F('first_team_goals')))
        return home_drawn.count() + away_drawn.count()

    def _get_games_lost(self, obj):
        home_lost = Match.objects.filter(Q(first_team__id=obj.id) & Q(first_team_goals__lt=F('second_team_goals')))
        away_lost = Match.objects.filter(Q(second_team__id=obj.id) & Q(second_team_goals__lt=F('first_team_goals')))
        return home_lost.count() + away_lost.count()

    def _get_goals_scored(self, obj):
        home_played = Match.objects.filter(Q(first_team__id=obj.id))
        away_played = Match.objects.filter(Q(second_team__id=obj.id))
        home_scored = home_played.aggregate(goals=Coalesce(Sum('first_team_goals', output_field=IntegerField()), 0))
        away_scored = away_played.aggregate(goals=Coalesce(Sum('second_team_goals', output_field=IntegerField()), 0))
        return home_scored['goals'] + away_scored['goals']

    def _get_goals_lost(self, obj):
        home_played = Match.objects.filter(Q(first_team__id=obj.id))
        away_played = Match.objects.filter(Q(second_team__id=obj.id))
        home_lost = home_played.aggregate(goals=Coalesce(Sum('second_team_goals', output_field=IntegerField()), 0))
        away_lost = away_played.aggregate(goals=Coalesce(Sum('first_team_goals', output_field=IntegerField()), 0))
        return home_lost['goals'] + away_lost['goals']


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team


class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
