from rest_framework import serializers
from .models import Product, Cart, CartItem, Order, OrderItem

# ---------------- Product Serializer ----------------
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'stock', 'created_at']


# ---------------- Cart Item Serializer ----------------
class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price']

    total_price = serializers.SerializerMethodField()

    def get_total_price(self, obj):
        return obj.product.price * obj.quantity


# ---------------- Cart Serializer ----------------
class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'total']

    def get_total(self, obj):
        return sum(item.product.price * item.quantity for item in obj.items.all())


# ---------------- Order Item Serializer ----------------
class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'total_price']

    total_price = serializers.SerializerMethodField()

    def get_total_price(self, obj):
        return obj.product.price * obj.quantity


# ---------------- Order Serializer ----------------
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'user', 'created_at', 'items', 'total']

    def get_total(self, obj):
        return sum(item.product.price * item.quantity for item in obj.items.all())