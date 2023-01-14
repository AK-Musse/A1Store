from django.shortcuts import render, redirect
from .models import Product, Photo, Order, Cart
from django.shortcuts import redirect, render
from django.http import HttpResponse
import boto3
from django.views import generic
import uuid
import traceback
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
# Import the mixin for class-based views
from django.contrib.auth.mixins import LoginRequiredMixin

S3_BASE_URL = 'https://s3-us-east-2.amazonaws.com/'
BUCKET = 'sb-a1store'


def find_logged_user_details(request):
  return {
    'id' : request.user.id,
    'username' : request.user.username,
    'is_superuser' : request.user.is_superuser,
    'date_joined' : request.user.date_joined
  }


def home(request):
  logged_in_user = request.user
  total = Cart.objects.filter(user_id = logged_in_user.id).count()
  products = Product.objects.all()
  return render(request, 'product/home.html',
  { 
    'products' : products, 
    'total' : total
  })


@login_required(login_url='/accounts/login/')     
def product_create(request):
  if request.method == 'POST':
    product = Product.objects.create(
      name=request.POST.get('product_name'),
      description=request.POST.get('product_description'),
      price=request.POST.get('product_price'),
      category=request.POST.get('product_category')
      )
    product.save()
    print(product.id)
    # photo-file was the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
      s3 = boto3.client('s3')
      # need a unique "key" for S3 / needs image file extension too
      key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
      # just in case something goes wrong
      try:
        s3.upload_fileobj(photo_file, BUCKET, key)
        # build the full url string
        url = f"{S3_BASE_URL}{BUCKET}/{key}"
        # we can assign to cat_id or cat (if you have a cat object)
        photo = Photo(url=url, product_id=product.id)
        photo.save()
      except:
        print('An error occurred uploading file to S3')
    return redirect('main_app:home')
  else:
    return render(request,'product/create.html')


def product_details(request, prod_id):
  logged_in_user_id = find_logged_user_details(request).get('id')
  total = Cart.objects.filter(user_id = logged_in_user_id).count()
  product = Product.objects.get(id=prod_id)
  return render(request, 'product/detail.html', 
  { 
    'product' : product, 
    'product_id' : prod_id,
    'total' : total
  })

# class CartCreate(LoginRequiredMixin, generic.CreateView):
#     model = Cart
#     # fields = '__all__'
#     success_url = '/products/'
#     fields = ['name', 'description', 'price', 'Category']

#     # This inherited method is called when a
#     # valid cat form is being submitted
#     def form_valid(self, form):
#       # Assign the logged in user (self.request.user)
#       form.instance.user = self.request.user  # form.instance is the cat
#       # Let the CreateView do its job as usual
#       return super().form_valid(form) 

@login_required(login_url='/accounts/login/')     
def add_to_cart(request, prod_id):
  logged_in_user_id = find_logged_user_details(request).get('id')
  product = Product.objects.get(id=prod_id)
  item_exist_in_cart = Cart.objects.filter( product_id = product.id, user_id = logged_in_user_id )
  if item_exist_in_cart:
    existing_quantity = item_exist_in_cart[0].quantity   
    new_quantity = existing_quantity + 1 
    Cart.objects.filter( product_id = product.id, user_id = logged_in_user_id).update(quantity = new_quantity)
  else:
    cart = Cart.objects.create(product_id = product.id, user_id = logged_in_user_id)
    cart.save()
  
  return render(request, 'product/detail.html', 
  {
    'product' : product,
    'product_id' : prod_id,
    'total_items_in_cart' : calculate_total_items_in_cart(request)
  })


def calculate_total_items_in_cart(request):
  logged_in_user = request.user
  products_in_cart = Cart.objects.filter(user_id = logged_in_user.id)
  print(products_in_cart)
  total_quantity = 0
  for product in products_in_cart:
      total_quantity += product.quantity
  return total_quantity


def cart(request):
  logged_in_user_id = find_logged_user_details(request).get('id')
  tuples_of_all_items_in_cart = Cart.objects.filter(user_id = logged_in_user_id).values_list('product_id', 'quantity')
  items_in_cart, quantity = zip(*tuples_of_all_items_in_cart)
  products_in_cart = Product.objects.filter(id__in = items_in_cart) 
  modified_products_list = []

  index_of_modified_products_list = 0
  subtotal = 0
  def convert_model_to_list(product):
    return {
      'id': product.pk,
      'name': product.name,
      'description': product.description,
      'price': product.price,
      'category': product.category,
      'quantity': None
    }

  for product in list(products_in_cart):
    for pair_of_prod_id_and_quantity in tuples_of_all_items_in_cart:
      print(tuples_of_all_items_in_cart)
      if product.pk == pair_of_prod_id_and_quantity[0]:
        modified_products_list.append(convert_model_to_list(product))
        modified_products_list[index_of_modified_products_list]['quantity'] = pair_of_prod_id_and_quantity[1]
        subtotal += float(modified_products_list[index_of_modified_products_list]['price'] * modified_products_list[index_of_modified_products_list]['quantity'])
        index_of_modified_products_list += 1 
   
  tax =  13 / 100 * subtotal
  prod_total = subtotal + tax
  return render(request, 'cart.html', 
  {
    'products': modified_products_list,
    'subtotal' : subtotal,
    'tax' : tax,
    'prod_total' : prod_total,
    'total_items_in_cart' : calculate_total_items_in_cart(request)
  })



  
def cart_checkout(request):
  logged_in_user_id = find_logged_user_details(request).get('id')
  checked_out_products = Cart.objects.filter(user_id = logged_in_user_id)
  print("checkout")
  checked_out_products.delete()
  # total = Cart.objects.filter(user_id = logged_in_user_id).count()
  print(f'Deleted products are : \n {checked_out_products}')
  return redirect('main_app:home')


def signup(request):
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      logged_in_user_id = find_logged_user_details(request).get('id')
      # created_new_cart_of_user = Cart.objects.create(user_id = logged_in_user_id)
      return redirect('main_app:home')  
      # or
      # return redirect('product/home.html')
  else:
    form = UserCreationForm()
  return render(request, 'registration/signup.html', 
  {
    'form': form
  })