from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView, FormView, View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import login
from .models import Product, Cart, CartItem, Order, OrderItem
from .forms import ProductForm, OrderForm, CustomerRegisterForm

# REST Framework
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .serializers import ProductSerializer, CartSerializer, OrderSerializer


# ---------------- Pages ----------------
class HomePageView(ListView):
    model = Product
    template_name = 'products/home.html'
    context_object_name = 'products'
    ordering = ['-id']


class ProductCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/add_product.html'
    success_url = '/'

    def form_valid(self, form):
        messages.success(self.request, "تم إضافة المنتج بنجاح.")
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.is_staff


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/edit_product.html'
    success_url = '/'

    def form_valid(self, form):
        messages.success(self.request, "تم تعديل المنتج.")
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.is_staff


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    template_name = 'products/delete_product.html'
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        messages.success(request, "تم حذف المنتج.")
        return super().delete(request, *args, **kwargs)

    def test_func(self):
        return self.request.user.is_staff


class CartView(LoginRequiredMixin, TemplateView):
    template_name = 'products/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        total = sum(item.product.price * item.quantity for item in cart.items.all())
        context['cart'] = cart
        context['total'] = total
        return context


class AddToCartView(LoginRequiredMixin, View):
    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += 1
        cart_item.save()
        messages.success(request, f"تمت إضافة {product.name} إلى السلة.")
        return redirect('view_cart')


class RemoveFromCartView(LoginRequiredMixin, View):
    def get(self, request, item_id):
        cart = Cart.objects.get(user=request.user)
        item = get_object_or_404(CartItem, id=item_id, cart=cart)
        item.delete()
        messages.success(request, "تم حذف المنتج من السلة.")
        return redirect('view_cart')


class CheckoutView(LoginRequiredMixin, FormView):
    template_name = 'products/checkout.html'
    form_class = OrderForm
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = Cart.objects.filter(user=self.request.user).first()
        total = sum(item.product.price * item.quantity for item in cart.items.all()) if cart else 0
        context['cart'] = cart
        context['total'] = total
        return context

    def form_valid(self, form):
        cart = Cart.objects.filter(user=self.request.user).first()
        if not cart or not cart.items.exists():
            messages.error(self.request, "السلة فارغة.")
            return redirect('home_page')
        order = form.save(commit=False)
        order.user = self.request.user
        order.save()
        for item in cart.items.all():
            OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)
        cart.delete()
        messages.success(self.request, "تم تأكيد الطلب بنجاح.")
        return super().form_valid(form)


class RegisterView(CreateView):
    form_class = CustomerRegisterForm
    template_name = 'products/register.html'
    success_url = '/'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)  # تسجيل دخول مباشر بعد التسجيل
        messages.success(self.request, "تم إنشاء الحساب وتسجيل الدخول بنجاح.")
        return super().form_valid(form)


class MyOrdersView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'products/my_orders.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')


# ---------------- APIs ----------------
class ProductListCreateAPI(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]  # أي مستخدم مسجل يستطيع رؤية المنتجات
    # لإضافة/تعديل المنتجات فقط للـ Admin، يمكن تعديل serializer أو استخدام IsAdminUser مع POST/PUT


class ProductDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]  # أي مستخدم مسجل، تعديل وحذف ممكن تحكمه لاحقاً


class CartListAPI(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return cart


class OrderListCreateAPI(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class OrderDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
