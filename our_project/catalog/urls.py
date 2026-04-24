from django.urls import path
from . import views
from . import api


app_name = 'catalog'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('category/<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart_view, name='cart_view'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:product_id>/', views.update_cart, name='update_cart'),  # ← ДОБАВИ ЭТУ СТРОКУ!
    path('toggle-theme/', views.toggle_theme, name='toggle_theme'),
]

# API endpoints
urlpatterns += [
    path('api/categories/', api.CategoryListView.as_view(), name='api_category_list'),
    path('api/categories/<int:id>/', api.CategoryDetailView.as_view(), name='api_category_detail'),
    path('api/products/', api.ProductListView.as_view(), name='api_product_list'),
    path('api/products/<int:id>/', api.ProductDetailView.as_view(), name='api_product_detail'),
]