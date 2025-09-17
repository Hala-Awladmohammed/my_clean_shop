from django.urls import path
from .views import (
    HomePageView, ProductCreateView, ProductUpdateView, ProductDeleteView,
    CartView, AddToCartView, RemoveFromCartView, CheckoutView,
    ProductListCreateAPI, ProductDetailAPI, CartListAPI, OrderListCreateAPI,
    OrderDetailAPI, RegisterView, MyOrdersView
)

urlpatterns = [
    # ---------- Pages ----------
    path('', HomePageView.as_view(), name='home_page'),
    path('products/', HomePageView.as_view(), name='home_page'),

    path('products/add/', ProductCreateView.as_view(), name='add_product'),
    path('products/<int:pk>/edit/', ProductUpdateView.as_view(), name='edit_product'),
    path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name='delete_product'),

    path('cart/', CartView.as_view(), name='view_cart'),
    path('cart/add/<int:product_id>/', AddToCartView.as_view(), name='add_to_cart'),
    path('cart/remove/<int:item_id>/', RemoveFromCartView.as_view(), name='remove_from_cart'),

    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('my-orders/', MyOrdersView.as_view(), name='my_orders'),

    # ---------- APIs ----------
    # Products API
    path('api/products/', ProductListCreateAPI.as_view(), name='api_products'),          # GET all, POST new
    path('api/products/<int:pk>/', ProductDetailAPI.as_view(), name='api_product_detail'),  # GET, PUT, DELETE

    # Cart API
    path('api/cart/', CartListAPI.as_view(), name='api_cart'),  # GET cart items (تم السماح للجميع)

    # Orders API
    path('api/orders/', OrderListCreateAPI.as_view(), name='api_orders'),                # GET all user orders, POST order
    path('api/orders/<int:pk>/', OrderDetailAPI.as_view(), name='api_order_detail'),      # GET, PUT, DELETE single order
]
