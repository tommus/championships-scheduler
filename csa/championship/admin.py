from django.contrib import admin
from csa.championship import models


class ParticipationAdmin(admin.ModelAdmin):
    list_filter = ('player__username',)


admin.site.register(models.Team)
admin.site.register(models.Participation, ParticipationAdmin)
admin.site.register(models.Championship)
