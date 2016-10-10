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
        return str("{} - {}".format(self.championship.name, self.name))

    class Meta:
        verbose_name = _('Group')
        verbose_name_plural = _('Groups')


class Match(Model):
    group = ForeignKey(Group, verbose_name=_('group'))
    host_team = ForeignKey(
        Participation,
        related_name='match_host_team',
        verbose_name=_('host_team'),
        blank=False
    )
    guest_team = ForeignKey(
        Participation,
        related_name='match_guest_team',
        verbose_name=_('guest_team'),
        blank=False
    )
    host_team_goals = IntegerField(verbose_name=_('host_team_goals'), blank=True, null=True)
    guest_team_goals = IntegerField(verbose_name=_('guest_team_goals'), blank=True, null=True)

    def __str__(self):
        return str('{} ({}) - ({}) {}'.format(
            self.host_team,
            self.host_team_goals if self.host_team_goals is not None else '',
            self.guest_team_goals if self.guest_team_goals is not None else '',
            self.guest_team
        ))

    class Meta:
        verbose_name = _('Match')
        verbose_name_plural = _('Matches')
