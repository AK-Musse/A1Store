from django.urls import path, include
from . import views

app_name = "main_app"

urlpatterns = [
    path('', views.home, name='home'),
    path('products/<int:prod_id>', views.product_details, name='detail'),
    path('products/<int:prod_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', views.signup, name='signup'),
    path('product/create/', views.product_create, name='product_create'),
    path('cart/', views.cart_checkout, name='cart_checkout')




    # path('about/', views.about, name='about'),
    # path('cats/', views.cats_index, name='index'),
    # # path('cats/', views.CatList.as_view(), name='index'),
    # path('cats/create/', views.CatCreate.as_view(), name='cats_create'),
    # path('cats/<int:pk>/update/', views.CatUpdate.as_view(), name='cats_update'),
    # path('cats/<int:pk>/delete/', views.CatDelete.as_view(), name='cats_delete'),
    # path('cats/<int:cat_id>/add_feeding/', views.add_feeding, name='add_feeding'),
    # path('cats/<int:cat_id>/assoc_toy/<int:toy_id>/', views.assoc_toy, name='assoc_toy'),
    # path('cats/create/', views.CatCreate.as_view(), name='cats_create'),

    # New url pattern below
    #path('accounts/signup/', views.signup, name='signup'),
]