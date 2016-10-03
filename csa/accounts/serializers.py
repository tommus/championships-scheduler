from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    groups = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'groups')

    def get_groups(self, obj):
        groups = obj.groups.all()
        return [group.name for group in groups]


class UserSimpleSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username')
