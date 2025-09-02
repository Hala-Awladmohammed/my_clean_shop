from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView, FormView, View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Product, Cart, CartItem, Order, OrderItem
from .forms import ProductForm, OrderForm
from rest_framework import generics
from .serializers import ProductSerializer, CartSerializer, OrderSerializer, OrderItemSerializer

# ---------------- صفحات الويب ----------------

class HomePageView(ListView):
    model = Product
    template_name = 'products/home.html'
    context_object_name = 'products'
    ordering = ['-id']

# ---- حماية صفحات إدارة المنتجات ----
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
        messages.success(self.request, "تم حذف المنتج.")
        return super().delete(request, *args, **kwargs)

    def test_func(self):
        return self.request.user.is_staff

# ---------------- سلة المشتريات ----------------
class CartView(TemplateView):
    template_name = 'products/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get('cart_id')
        cart = Cart.objects.filter(id=cart_id).first() if cart_id else None
        total = sum(item.product.price * item.quantity for item in cart.items.all()) if cart else 0
        context['cart'] = cart
        context['total'] = total
        return context

class AddToCartView(View):
    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        cart_id = request.session.get('cart_id')
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
        else:
            cart = Cart.objects.create()
            request.session['cart_id'] = cart.id
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += 1
        cart_item.save()
        messages.success(request, f"تمت إضافة {product.name} إلى السلة.")
        return redirect('view_cart')

class RemoveFromCartView(View):
    def get(self, request, item_id):
        cart_id = request.session.get('cart_id')
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
            item = get_object_or_404(CartItem, id=item_id, cart=cart)
            item.delete()
            messages.success(request, "تم حذف المنتج من السلة.")
        return redirect('view_cart')

# ---------------- Checkout ----------------
class CheckoutView(FormView):
    template_name = 'products/checkout.html'
    form_class = OrderForm
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get('cart_id')
        cart = Cart.objects.filter(id=cart_id).first() if cart_id else None
        total = sum(item.product.price * item.quantity for item in cart.items.all()) if cart else 0
        context['cart'] = cart
        context['total'] = total
        return context

    def form_valid(self, form):
        cart_id = self.request.session.get('cart_id')
        if not cart_id:
            messages.error(self.request, "السلة فارغة.")
            return redirect('home_page')
        cart = Cart.objects.get(id=cart_id)
        order = form.save()
        for item in cart.items.all():
            OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)
        cart.delete()
        self.request.session['cart_id'] = None
        messages.success(self.request, "تم تأكيد الطلب بنجاح.")
        return super().form_valid(form)

# ---------------- APIs ----------------
class ProductListCreateAPI(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class CartListAPI(generics.RetrieveAPIView):
    serializer_class = CartSerializer

    def get_object(self):
        cart_id = self.request.session.get('cart_id')
        return Cart.objects.filter(id=cart_id).first()

class OrderListCreateAPI(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
