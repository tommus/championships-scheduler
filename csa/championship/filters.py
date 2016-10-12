from django_filters.filterset import FilterSet, NumberFilter

from csa.championship.models import Match


class MatchFilterSet(FilterSet):
    championship = NumberFilter(name='group__championship')

    class Meta:
        model = Match
        fields = ['championship']
