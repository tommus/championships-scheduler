from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer, SerializerMethodField


class UserSerializer(ModelSerializer):
    groups = SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'groups')

    def get_groups(self, obj):
        groups = obj.groups.all()
        return [group.name for group in groups]


class UserSimpleSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')
