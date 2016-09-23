from django.contrib import admin
from csa.schedule import models


class MatchAdmin(admin.ModelAdmin):
    list_filter = ('championship__name',)

    # Add filters:
    #     - by player
    #     - by played


class GroupAdmin(admin.ModelAdmin):
    list_filter = ('championship__name',)


admin.site.register(models.Match, MatchAdmin)
admin.site.register(models.Group, GroupAdmin)
