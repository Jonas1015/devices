from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name = 'home'),
    path('catalog/', catalog, name = 'catalog'),
    path('message/', message, name = 'message'),
    path('order/', order, name = 'order'),
    path('make/order/<int:id>/', make_order, name = 'make-order'),
    # path('categories/', CategoryListView.as_view(), name = 'categories'),

    # CATEGORIES
    path('categories/', categoriesList, name = 'categories'),
    path('create-category/', create_category, name = 'create-category'),
    path('update-categoy/<int:id>/', update_category, name = 'update-category'),
    path('delete-category/<int:id>/', delete_category, name = 'delete-category'),

    # PRODUCTS
    path('products/', productsList, name = 'products'),
    path('create-product/', create_product, name = 'create-product'),
    path('update-product/<int:id>/', update_product, name = 'update-product'),
    path('delete-product/<int:id>/', delete_product, name = 'delete-product'),
]
