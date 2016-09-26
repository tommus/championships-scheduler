import random
import itertools
from string import ascii_uppercase
from django.contrib import admin
from csa.championship import models


class ParticipationAdmin(admin.ModelAdmin):
    list_filter = ('player__username',)


class ChampionshipAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        championship = form.save(commit=True)

        self._prepare_groups(championship)
        self._prepare_matches(championship)

    def _prepare_groups(self, championship):
        championship_participates = models.Participation.objects.filter(championship__name=championship.name)
        human_players = list(set([participate.player for participate in championship_participates]))

        available_participates = list(championship_participates)

        for i in range(championship.groups):
            group_name = ascii_uppercase[i]
            group_participates = []

            group = models.Group(
                championship=championship,
                name=group_name,
            )
            group.save()

            for player in human_players:
                available_player_teams = [p for p in available_participates if p.player.id==player.id]

                if len(available_player_teams) < championship.players_per_group:
                    selected_player_teams = available_player_teams
                else:
                    selected_player_teams = random.sample(available_player_teams, championship.players_per_group)

                [group_participates.append(t) for t in selected_player_teams]
                available_participates = [p for p in available_participates if p not in selected_player_teams]

            for participate in group_participates:
                group.participates.add(participate)

    def _prepare_matches(self, championship):
        groups = models.Group.objects.filter (championship__name=championship.name)

        for group in groups:
            group_participates = models.Participation.objects.filter(group=group)
            pairs = list(itertools.combinations(group_participates, 2))
            random.shuffle(pairs)

            for pair in pairs:
                if pair[0].player != pair[1].player:
                    match = models.Match(
                        championship=championship,
                        first_team=pair[0],
                        second_team=pair[1]
                    )
                    match.save()

            if championship.home_and_away:
                for pair in pairs:
                    if pair[0].player != pair[1].player:
                        match = models.Match(
                            championship=championship,
                            first_team=pair[1],
                            second_team=pair[0]
                        )
                        match.save()


class MatchAdmin(admin.ModelAdmin):
    list_filter = ('championship__name',)


class GroupAdmin(admin.ModelAdmin):
    list_filter = ('championship__name',)


admin.site.register(models.Team)
admin.site.register(models.Participation, ParticipationAdmin)
admin.site.register(models.Championship, ChampionshipAdmin)
admin.site.register(models.Match, MatchAdmin)
admin.site.register(models.Group, GroupAdmin)
