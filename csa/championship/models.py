from django.contrib.auth import models as auth_models
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Team(models.Model):
    name = models.CharField(max_length=50, verbose_name=_('name'), blank=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Team')
        verbose_name_plural = _('Teams')


class Participation(models.Model):
    player = models.ForeignKey(auth_models.User, verbose_name=_('player'))
    team = models.ForeignKey(Team, verbose_name=_('team'))

    def __str__(self):
        return str('{} ({})'.format(self.team, self.player.username))

    class Meta:
        verbose_name = _('Participation')
        verbose_name_plural = _('Participation')


class Championship(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('name'))
    participates = models.ManyToManyField(Participation, verbose_name=_('participates'))
    groups = models.IntegerField(default=1, verbose_name=_('groups'))
    players_per_group = models.IntegerField(default=1, verbose_name=_('players_per_group'))
    home_and_away = models.BooleanField(default=True, verbose_name=_('home_and_away'))

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = _('Championship')
        verbose_name_plural = _('Championships')


class Match(models.Model):
    championship = models.ForeignKey(Championship, verbose_name=_('championship'))
    first_team = models.ForeignKey(
        Participation,
        related_name='match_first_team',
        verbose_name=_('first_team'),
        blank=False
    )
    second_team = models.ForeignKey(
        Participation,
        related_name='match_second_team',
        verbose_name=_('second_team'),
        blank=False
    )
    first_team_home = models.BooleanField(default=True, verbose_name=_('first_team_home'))
    second_team_home = models.BooleanField(default=False, verbose_name=_('second_team_home'))
    first_team_goals = models.IntegerField(verbose_name=_('first_team_goals'), blank=True, null=True)
    second_team_goals = models.IntegerField(verbose_name=_('second_team_goals'), blank=True, null=True)

    def __str__(self):
        return str('{} ({}) - ({}) {}'.format(
            self.first_team,
            self.first_team_goals if self.first_team_goals is not None else '',
            self.second_team_goals if self.second_team_goals is not None else '',
            self.second_team
        ))

    class Meta:
        verbose_name = _('Match')
        verbose_name_plural = _('Matches')


class Group(models.Model):
    championship = models.ForeignKey(Championship, verbose_name=_('championship'), blank=True, null=True)
    name = models.CharField(max_length=1, verbose_name=_('name'))
    participates = models.ManyToManyField(Participation, verbose_name=_('participates'))

    def __str__(self):
        return str('{} - {}'.format(self.championship, self.name))

    class Meta:
        verbose_name = _('Group')
        verbose_name_plural = _('Groups')


class Result(models.Model):
    team = models.ForeignKey(Participation, verbose_name=_('team'))
    group = models.ForeignKey(Group, verbose_name=_('group'))
    won = models.IntegerField(default=0, verbose_name=_('won'))
    drawn = models.IntegerField(default=0, verbose_name=_('drawn'))
    lost = models.IntegerField(default=0, verbose_name=_('lost'))
    goals_scored = models.IntegerField(default=0, verbose_name=_('goals_scored'))
    goals_lost = models.IntegerField(default=0, verbose_name=_('goals_lost'))

    def __str__(self):
        return str('{} - {} - {}'.format(self.group.championship, self.group.name, self.team))

    class Meta:
        verbose_name = _('Result')
        verbose_name_plural = _('Results')
