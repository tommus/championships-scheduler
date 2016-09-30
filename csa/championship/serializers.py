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


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team


class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
