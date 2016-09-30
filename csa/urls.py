from django.conf.urls import include, url
from django.contrib import admin
from rest_framework import routers

from csa.accounts.views import LoginView, LogoutView
from csa.championship.views import ChampionshipViewSet, GroupViewSet, ParticipationViewSet, MatchViewSet, TeamViewSet

router = routers.DefaultRouter()
router.register(r'championship/championships', ChampionshipViewSet)
router.register(r'championship/groups', GroupViewSet)
router.register(r'championship/participates', ParticipationViewSet)
router.register(r'championship/matches', MatchViewSet)
router.register(r'championship/teams', TeamViewSet)

urlpatterns = [
    # ex: /
    url(r'', include('csa.webclient.urls')),

    # ex: /api/
    url(r'^api/', include(router.urls)),

    url(r'^api/login/', LoginView.as_view(), name='login'),
    url(r'^api/logout/', LogoutView.as_view(), name='logout'),

    # ex: /admin/
    url(r'^admin/', admin.site.urls),
]
