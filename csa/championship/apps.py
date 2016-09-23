from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ChampionshipConfig(AppConfig):
    name = 'csa.championship'
    verbose_name = _("Championship")
