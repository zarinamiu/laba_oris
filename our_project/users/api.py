from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth.models import User
from .models import Profile
from .serializers import UserSerializer, ProfileSerializer, UserRegisterSerializer


class UserListView(generics.ListAPIView):
    """API: Список всех пользователей"""
    queryset = User.objects.select_related('profile').all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Получить список всех пользователей",
        responses={200: UserSerializer(many=True)},
        tags=['Пользователи']
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class UserDetailView(generics.RetrieveAPIView):
    """API: Детальная информация о пользователе"""
    queryset = User.objects.select_related('profile').all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    lookup_field = 'id'

    @swagger_auto_schema(
        operation_description="Получить информацию о пользователе по ID",
        responses={200: UserSerializer()},
        tags=['Пользователи']
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class ProfileDetailView(generics.RetrieveAPIView):
    """API: Профиль текущего пользователя"""
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.profile

    @swagger_auto_schema(
        operation_description="Получить профиль текущего пользователя",
        responses={200: ProfileSerializer()},
        tags=['Профиль']
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class UserRegisterView(generics.CreateAPIView):
    """API: Регистрация нового пользователя"""
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Регистрация нового пользователя",
        request_body=UserRegisterSerializer,
        responses={201: UserSerializer()},
        tags=['Пользователи']
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)