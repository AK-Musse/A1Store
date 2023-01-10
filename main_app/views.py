from django.shortcuts import render
from .models import Product, Order, Photo

# Create your views here.

def home(request):
  products = Product.objects.all()

  return render(request, 'product/homepage.html', { 'products' : products})