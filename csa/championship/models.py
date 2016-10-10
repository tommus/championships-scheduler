from django.contrib.auth.models import User
from django.db.models import (
    BooleanField,
    CharField,
    ForeignKey,
    IntegerField,
    ManyToManyField,
    Model
)
from django.utils.translation import ugettext_lazy as _


class Team(Model):
    name = CharField(max_length=50, verbose_name=_('name'), blank=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Team')
        verbose_name_plural = _('Teams')


class Championship(Model):
    name = CharField(max_length=100, verbose_name=_('name'))
    groups = IntegerField(default=1, verbose_name=_('groups'))
    players = ManyToManyField(User, verbose_name=_('player'))
    teams = ManyToManyField(Team, verbose_name=_('team'))
    home_and_away = BooleanField(default=True, verbose_name=_('home_and_away'))

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = _('Championship')
        verbose_name_plural = _('Championships')


class Participation(Model):
    player = ForeignKey(User, verbose_name=_('player'))
    team = ForeignKey(Team, verbose_name=_('team'))
    championship = ForeignKey(Championship, verbose_name=_('championship'))

    def __str__(self):
        return str('{} ({})'.format(self.team, self.player.username))

    class Meta:
        verbose_name = _('Participation')
        verbose_name_plural = _('Participation')


class Group(Model):
    championship = ForeignKey(Championship, verbose_name=_('championship'), blank=True, null=True)
    name = CharField(max_length=1, verbose_name=_('name'))
    participates = ManyToManyField(Participation, verbose_name=_('participates'))

    def __str__(self):
        return str('{} - {}'.format(self.championship, self.name))

    class Meta:
        verbose_name = _('Group')
        verbose_name_plural = _('Groups')


class Match(Model):
    group = ForeignKey(Group, verbose_name=_('group'))
    first_team = ForeignKey(
        Participation,
        related_name='match_first_team',
        verbose_name=_('first_team'),
        blank=False
    )
    second_team = ForeignKey(
        Participation,
        related_name='match_second_team',
        verbose_name=_('second_team'),
        blank=False
    )
    first_team_home = BooleanField(default=True, verbose_name=_('first_team_home'))
    second_team_home = BooleanField(default=False, verbose_name=_('second_team_home'))
    first_team_goals = IntegerField(verbose_name=_('first_team_goals'), blank=True, null=True)
    second_team_goals = IntegerField(verbose_name=_('second_team_goals'), blank=True, null=True)

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
