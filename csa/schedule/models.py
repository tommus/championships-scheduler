from django.db import models
from django.utils.translation import ugettext_lazy as _

from csa.championship import models as champ_models


class Match(models.Model):
    championship = models.ForeignKey(champ_models.Championship, verbose_name=_("championship"), blank=False)
    first_team = models.ForeignKey(
        champ_models.Participation,
        related_name='match_first_team',
        verbose_name=_("first_team"),
        blank=False
    )
    second_team = models.ForeignKey(
        champ_models.Participation,
        related_name='match_second_team',
        verbose_name=_("second_team"),
        blank=False
    )
    first_team_home = models.BooleanField(default=True, verbose_name=_("first_team_home"), blank=False)
    second_team_home = models.BooleanField(default=False, verbose_name=_("second_team_home"), blank=False)
    first_team_goals = models.IntegerField(verbose_name=_("first_team_goals"), blank=True, null=True)
    second_team_goals = models.IntegerField(verbose_name=_("second_team_goals"), blank=True, null=True)

    def __str__(self):
        return str("{} ({}) - ({}) {}".format(
            self.first_team,
            self.first_team_goals if self.first_team_goals is not None else '',
            self.second_team_goals if self.second_team_goals is not None else '',
            self.second_team
        ))

    class Meta:
        verbose_name = _("Match")
        verbose_name_plural = _("Matches")


class Group(models.Model):
    championship = models.ForeignKey(champ_models.Championship, verbose_name=_("championship"), null=True)
    name = models.CharField(max_length=1, verbose_name=_("name"), blank=False)

    def __str__(self):
        return str("{} - {}".format(self.championship, self.name))

    class Meta:
        verbose_name = _("Group")
        verbose_name_plural = _("Groups")


class Result(models.Model):
    team = models.ForeignKey(champ_models.Participation, verbose_name=_("team"), blank=False)
    group = models.ForeignKey(Group, verbose_name=_("group"), blank=False)
    won = models.IntegerField(default=0, verbose_name=_("won"), blank=False)
    drawn = models.IntegerField(default=0, verbose_name=_("drawn"), blank=False)
    lost = models.IntegerField(default=0, verbose_name=_("lost"), blank=False)
    goals_scored = models.IntegerField(default=0, verbose_name=_("goals_scored"), blank=False)
    goals_lost = models.IntegerField(default=0, verbose_name=_("goals_lost"), blank=False)

    def __str__(self):
        return str("{} - {} - {}".format(self.group.championship, self.group.name, self.team))

    class Meta:
        verbose_name = _("Result")
        verbose_name_plural = _("Results")
