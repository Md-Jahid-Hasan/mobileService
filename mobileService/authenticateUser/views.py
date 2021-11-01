from django.db.models import query
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView, ListAPIView
from rest_framework.mixins import ListModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken, OutstandingToken, BlacklistedToken
from django.contrib.auth import get_user_model as User


from subscription.models import Number
from .serializers import MyTokenObtainPairSerializer, UserCreateSerializer, UserDetailsSerializer,\
                         UserNumberUpdateSerializer
from subscription.serializers import NumberSerializer


class LoginView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class UserCreateView(CreateAPIView, TokenObtainPairView):
    serializer_class = UserCreateSerializer


class RetrieveUserView(RetrieveAPIView):
    serializer_class = UserDetailsSerializer
    permission_classes = (IsAuthenticated, )

    def get_object(self):
        return self.request.user


class UpdateUserPNumber(ListAPIView, UpdateAPIView):
    """Change user primary number. Change serializer class based on request method also sending available
    number of authenticated user"""
    serializer_class = NumberSerializer
    queryset = Number.objects.all()

    def get_serializer_class(self):
        if self.request.method == "PUT":
            return UserNumberUpdateSerializer
        return self.serializer_class

    def get_queryset(self):
        return Number.objects.filter(user=self.request.user)
    
    def get_object(self):
        return self.request.user


class LogOutView(APIView):
    """Log out usr from current browser"""
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        refresh_token = request.data['refresh']
        token = RefreshToken(refresh_token)
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class LogOutAllView(APIView):
    """Log out usr from all available browser browser"""
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        tokens = OutstandingToken.objects.filter(user_id=request.user.id)
        for token in tokens:
            t, _ = BlacklistedToken.objects.get_or_create(token=token)
        return Response(status=status.HTTP_205_RESET_CONTENT)





