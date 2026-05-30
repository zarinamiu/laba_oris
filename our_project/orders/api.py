from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_yasg.utils import swagger_auto_schema
from .models import Order
from .serializers import OrderSerializer, OrderCreateSerializer


class OrderListView(generics.ListAPIView):
    """API: Список заказов текущего пользователя"""
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related('items__product').order_by('-created_at')  # Добавлен order_by

    @swagger_auto_schema(
        operation_description="Получить список заказов текущего пользователя",
        responses={200: OrderSerializer(many=True)},
        tags=['Заказы']
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class OrderDetailView(generics.RetrieveAPIView):
    """API: Детальная информация о заказе"""
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related('items__product').order_by('-created_at')  # Добавлен order_by

    @swagger_auto_schema(
        operation_description="Получить информацию о заказе по ID",
        responses={200: OrderSerializer()},
        tags=['Заказы']
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class OrderCreateView(generics.CreateAPIView):
    """API: Создание нового заказа"""
    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Создать новый заказ (требуется авторизация)",
        request_body=OrderCreateSerializer,
        responses={201: OrderSerializer()},
        tags=['Заказы']
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class OrderAllListView(generics.ListAPIView):
    """API: Список всех заказов (для админов)"""
    serializer_class = OrderSerializer
    permission_classes = [AllowAny]  # Можно заменить на IsAdminUser
    queryset = Order.objects.all().prefetch_related('items__product').select_related('user').order_by('-created_at')  # Добавлен order_by

    @swagger_auto_schema(
        operation_description="Получить список всех заказов",
        responses={200: OrderSerializer(many=True)},
        tags=['Заказы']
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)