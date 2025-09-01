from django.urls import path
from .views import (
    HomePageView, ProductCreateView, ProductUpdateView,
    ProductDeleteView, OrderCreateView,
    ProductListCreateAPI, ProductDetailAPI,
    OrderListCreateAPI, OrderDetailAPI
)

urlpatterns = [
    path('', HomePageView.as_view(), name='home_page'),
    path('products/add/', ProductCreateView.as_view(), name='add_product'),
    path('products/<int:pk>/edit/', ProductUpdateView.as_view(), name='edit_product'),
    path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name='delete_product'),
    path('order/<int:product_id>/', OrderCreateView.as_view(), name='order_product'),

    path('api/products/', ProductListCreateAPI.as_view(), name='api_products'),
    path('api/products/<int:pk>/', ProductDetailAPI.as_view(), name='api_product_detail'),
    path('api/orders/', OrderListCreateAPI.as_view(), name='api_orders'),
    path('api/orders/<int:pk>/', OrderDetailAPI.as_view(), name='api_order_detail'),
]
