from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView
from .models import Product, Order
from .forms import ProductForm, OrderForm
from rest_framework import generics
from .serializers import ProductSerializer, OrderSerializer


class HomePageView(ListView):
    model = Product
    template_name = 'products/home.html'
    context_object_name = 'products'
    ordering = ['-id']


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/add_product.html'
    success_url = reverse_lazy('home_page')

    def form_valid(self, form):
        messages.success(self.request, "تم إضافة المنتج بنجاح.")
        return super().form_valid(form)


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/edit_product.html'
    success_url = reverse_lazy('home_page')

    def form_valid(self, form):
        messages.success(self.request, "تم تعديل المنتج.")
        return super().form_valid(form)


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'products/delete_product.html'
    success_url = reverse_lazy('home_page')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "تم حذف المنتج.")
        return super().delete(request, *args, **kwargs)


class OrderCreateView(FormView):
    template_name = 'products/order_form.html'
    form_class = OrderForm

    def dispatch(self, request, *args, **kwargs):
        self.product = get_object_or_404(Product, pk=kwargs['product_id'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        order = form.save(commit=False)
        order.product = self.product
        order.save()
        messages.success(self.request, "تم إرسال طلبك بنجاح.")
        return redirect('home_page')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = self.product
        return context

class ProductListCreateAPI(generics.ListCreateAPIView):
        queryset = Product.objects.all()
        serializer_class = ProductSerializer

class ProductDetailAPI(generics.RetrieveUpdateDestroyAPIView):
        queryset = Product.objects.all()
        serializer_class = ProductSerializer

class OrderListCreateAPI(generics.ListCreateAPIView):
        queryset = Order.objects.all()
        serializer_class = OrderSerializer

class OrderDetailAPI(generics.RetrieveUpdateDestroyAPIView):
        queryset = Order.objects.all()
        serializer_class = OrderSerializer

