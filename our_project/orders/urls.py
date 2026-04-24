from django.urls import path
from . import views
from . import api

app_name = 'orders'

urlpatterns = [
    path('', views.order_list, name='order_list'),
    path('create/', views.order_create, name='order_create'),
    path('<int:order_id>/', views.order_detail, name='order_detail'),
]

urlpatterns += [
    path('api/', api.OrderListView.as_view(), name='api_order_list'),
    path('api/all/', api.OrderAllListView.as_view(), name='api_order_all'),
    path('api/<int:id>/', api.OrderDetailView.as_view(), name='api_order_detail'),
    path('api/create/', api.OrderCreateView.as_view(), name='api_order_create'),
]