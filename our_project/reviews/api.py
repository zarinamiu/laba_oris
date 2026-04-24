from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_yasg.utils import swagger_auto_schema
from .models import Review
from .serializers import ReviewSerializer, ReviewCreateSerializer


class ReviewListView(generics.ListAPIView):
    """API: Список всех отзывов"""
    queryset = Review.objects.select_related('product', 'user').all()
    serializer_class = ReviewSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Получить список всех отзывов",
        responses={200: ReviewSerializer(many=True)},
        tags=['Отзывы']
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class ReviewDetailView(generics.RetrieveAPIView):
    """API: Детальная информация об отзыве"""
    queryset = Review.objects.select_related('product', 'user').all()
    serializer_class = ReviewSerializer
    permission_classes = [AllowAny]
    lookup_field = 'id'

    @swagger_auto_schema(
        operation_description="Получить информацию об отзыве по ID",
        responses={200: ReviewSerializer()},
        tags=['Отзывы']
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class ReviewCreateView(generics.CreateAPIView):
    """API: Создание нового отзыва"""
    queryset = Review.objects.all()
    serializer_class = ReviewCreateSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Создать новый отзыв (требуется авторизация)",
        request_body=ReviewCreateSerializer,
        responses={201: ReviewSerializer()},
        tags=['Отзывы']
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)