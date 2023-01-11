from django.shortcuts import render, redirect
from .models import Product, Order, Photo, Cart
from django.shortcuts import redirect, render
from django.http import HttpResponse
# from django.views import generic
from django.views import generic
import uuid
import traceback
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
# Import the mixin for class-based views
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

def home(request):
  products = Product.objects.all()

  return render(request, 'product/home.html', { 'products' : products})

def product_details(request, prod_id):
  product = Product.objects.get(id=prod_id)
  # print(" Product is : ", prod_id)
  # print(" Product is : ", product)
  return render(request, 'product/detail.html', {'product' : product})

class CartCreate(LoginRequiredMixin, generic.CreateView):
    model = Cart
    # fields = '__all__'
    success_url = '/products/'
    fields = ['name', 'description', 'price', 'Category']

    # This inherited method is called when a
    # valid cat form is being submitted
    def form_valid(self, form):
      # Assign the logged in user (self.request.user)
      form.instance.user = self.request.user  # form.instance is the cat
      # Let the CreateView do its job as usual
      return super().form_valid(form) 

def add_to_cart(request):
      pass


def cart(request):
  products = Product.objects.all()
  print(products)
  subtotal = 0
  for product in products:
      subtotal += product.price
  tax = subtotal % 13 * 100
  total = subtotal + tax
  return render(request, 'cart.html', {
      'products': products,
      'subtotal' : subtotal,
      'tax' : tax,
      'total' : total
    })

def signup(request):
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      form.save()
      return redirect('main_app:home')    #one way to redirect to different page
      # or
      # return redirect('product/home.html')
  else:
    form = UserCreationForm()
  return render(request, 'registration/signup.html', {'form': form})
          
def login_user(request):
  if request.method == 'POST':
    form = AuthenticationForm(data=request.POST)
    if form.is_valid():
      user = form.get_user()
      login(request, user)
      return redirect('main_app:home')    #one way to redirect to different page
      # or
      # return redirect('product/home.html')
  else:
    form = AuthenticationForm()
  return render(request, 'login.html', {'form': form})