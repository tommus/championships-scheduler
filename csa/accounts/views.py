from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from rest_framework import permissions, response, status, views
from rest_framework import viewsets

from csa.accounts import serializers


class LoginView(views.APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.UserSerializer

    @staticmethod
    def post(request):
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
                return response.Response(serialized.data)
            else:
                return response.Response(
                    {'detail': _('This account is inactive.')},
                    status=status.HTTP_401_UNAUTHORIZED
                )
        else:
            return response.Response(
                {'detail': _('Login or password invalid.')},
                status=status.HTTP_401_UNAUTHORIZED
            )


class LogoutView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.UserSerializer

    @staticmethod
    def post(request):
        logout(request)
        return response.Response({}, status=status.HTTP_204_NO_CONTENT)


class UserView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.UserSerializer

    @staticmethod
    def get(request):
        serialized = serializers.UserSerializer(
            request.user,
            context={'request': request}
        )
        return response.Response(serialized.data)

    @staticmethod
    def put(request):
        password = request.data.get('password')
        if password:
            user = request.user
            user.set_password(password)
            user.save()
            serialized = serializers.UserSerializer(
                request.user,
                context={'request': request}
            )
            return response.Response(serialized.data)
        return response.Response(
            {'password': _('This field may not be null.')},
            status=status.HTTP_400_BAD_REQUEST
        )


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = serializers.UserSimpleSerializer
