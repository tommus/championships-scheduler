from django.contrib.auth import models as auth_models
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Team(models.Model):
    name = models.CharField(max_length=50, verbose_name=_("name"), blank=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Team")
        verbose_name_plural = _("Teams")


class Participation(models.Model):
    player = models.ForeignKey(auth_models.User, verbose_name=_("player"))
    team = models.ForeignKey(Team, verbose_name=_("team"))

    def __str__(self):
        return str("{} ({})".format(self.team, self.player.username))

    class Meta:
        verbose_name = _("Participation")
        verbose_name_plural = _("Participation")


class Championship(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("name"))
    participation = models.ManyToManyField(Participation, verbose_name=_("participation"))
    groups = models.IntegerField(default=1, verbose_name=_("groups"))
    players_per_group = models.IntegerField(default=1, verbose_name=_("players_per_group"))
    home_and_away = models.BooleanField(default=True, verbose_name=_("home_and_away"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Championship")
        verbose_name_plural = _("Championships")
