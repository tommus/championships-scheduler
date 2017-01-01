from django.conf.urls import include, url
from django.contrib import admin
from rest_framework import routers

from csa.accounts.views import (
    LoginView,
    LogoutView,
    UserViewSet
)
from csa.championship.views import (
    ChampionshipViewSet,
    ScheduleChampionshipViewSet,
    GroupViewSet,
    ParticipationViewSet,
    ResultsViewSet,
    MatchViewSet,
    TeamViewSet
)

router = routers.DefaultRouter()
router.register(r'accounts/users', UserViewSet)
router.register(r'championships/championships', ChampionshipViewSet)
router.register(r'championships/schedule', ScheduleChampionshipViewSet, base_name='schedule')
router.register(r'championships/groups', GroupViewSet)
router.register(r'championships/participates', ParticipationViewSet)
router.register(r'championships/results', ResultsViewSet, base_name='results')
router.register(r'championships/matches', MatchViewSet)
router.register(r'championships/teams', TeamViewSet)

urlpatterns = [
    url(r'', admin.site.urls),
    url(r'^api/', include(router.urls)),
    url(r'^api/login', LoginView.as_view(), name='login'),
    url(r'^api/logout', LogoutView.as_view(), name='logout'),
]

admin.site.site_title = "Championships Scheduler"
admin.site.site_header = "Championships Scheduler"
