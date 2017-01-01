from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED
)
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from csa.accounts import serializers


class LoginView(APIView):
    permission_classes = [AllowAny]
    serializer_class = serializers.UserSerializer
    error_messages = {
        'inactive': _('This account is inactive.'),
        'invalid_credentials': _('Login or password invalid.')
    }

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                serialized = serializers.UserSerializer(
                    user,
                    context={'request': request}
                )
                return Response(serialized.data)
            else:
                return Response(
                    {
                        'message': {
                            'username': self.error_messages['inactive']
                        }
                    },
                    status=HTTP_401_UNAUTHORIZED
                )
        else:
            return Response(
                {
                    'message': {
                        'username': self.error_messages['invalid_credentials'],
                        'password': self.error_messages['invalid_credentials']
                    },
                },
                status=HTTP_401_UNAUTHORIZED
            )


class LogoutView(APIView):
    permission_classes = [AllowAny]
    serializer_class = serializers.UserSerializer

    @staticmethod
    def post(request):
        logout(request)
        return Response({}, status=HTTP_204_NO_CONTENT)


class UserView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.UserSerializer
    error_messages = {
        'null_password': _('This field may not be null.')
    }

    @staticmethod
    def get(request):
        serialized = serializers.UserSerializer(
            request.user,
            context={'request': request}
        )
        return Response(serialized.data)

    def put(self, request):
        password = request.data.get('password')
        if password:
            user = request.user
            user.set_password(password)
            user.save()
            serialized = serializers.UserSerializer(
                request.user,
                context={'request': request}
            )
            return Response(serialized.data)
        return Response(
            {
                'message': {
                    'password': self.error_messages['null_password']
                }
            },
            status=HTTP_400_BAD_REQUEST
        )


class UserViewSet(ModelViewSet):
    filter_fields = ['championship']
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = serializers.UserSimpleSerializer
