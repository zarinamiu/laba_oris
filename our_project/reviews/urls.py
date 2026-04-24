from django.urls import path
from . import views
from . import api

app_name = 'reviews'

urlpatterns = [
    path('', views.review_list, name='review_list'),
    path('product/<int:product_id>/add/', views.add_review, name='add_review'),
    path('<int:review_id>/edit/', views.edit_review, name='edit_review'),
    path('<int:review_id>/delete/', views.delete_review, name='delete_review'),
    path('add/<int:product_id>/', views.add_review, name='add_review'),
    path('delete/<int:review_id>/', views.delete_review, name='delete_review'),
]

urlpatterns += [
    path('api/', api.ReviewListView.as_view(), name='api_review_list'),
    path('api/<int:id>/', api.ReviewDetailView.as_view(), name='api_review_detail'),
    path('api/create/', api.ReviewCreateView.as_view(), name='api_review_create'),
]