from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import F, Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from accounts.models import CustomUser


from .models import *
from .forms import *
import os

# Create your views here.
def home(request):
    form = messageForm(request.POST or None)
    context={
        'form': form,
    }
    template_name = 'main/home.html'
    return render(request, template_name, context)


def catalog(request):
    products_list = Product.objects.all().order_by('category')

    for product in products_list:
        print(os.path.basename(product.image1.name))

    categories = Category.objects.all()
    form = messageForm(request.POST or None)

    if request.GET.get('product_q'):
        products_list = Product.objects.filter(Q(name__icontains = request.GET.get('product_q'))).order_by('name')
        if not products_list:
            products_list = Product.objects.all().order_by('category')
            messages.warning(request, f'Query Not Found')
    elif request.GET.get('category_q'):
        try:
            category = get_object_or_404(Category, name=request.GET.get('category_q'))
            products_list = Product.objects.filter(category = category.id).order_by('name')
        except:
            messages.warning(request, f'Query Not Found')



    page = request.GET.get('page', 1)

    paginator = Paginator(products_list, 6)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)


    print(len(products.object_list))


    context = {
        'all_pages': paginator.num_pages,
        'products': products,
        'categories': categories,
        'form': form,
    }
    template_name = 'main/catalog.html'
    return render(request, template_name, context)

    # CATEGORIES
@login_required
def categories(request):
    context = {}
    template_name = 'main/categories.html'
    return render(request, template_name, context)

@login_required
def categoriesList(request):
    categories = Category.objects.all()
    add_category_form = addCategoryForm(request.POST or None)

    template_name = 'main/categories.html'
    context = {
        'categories':categories,
        'add_category_form': add_category_form,
    }
    return render(request, template_name, context)
@login_required
def create_category(request):
    if request.method == "POST":
        form = addCategoryForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, f'Category Created Successfully!')
            return redirect('categories')
        else:
            messages.success(request, f'Error occured!')
            return redirect('categories')

@login_required
def update_category(request, id):
    if request.method == "POST":
        category_name = request.POST.get('name')
        category = Category.objects.get(id = id)
        category.name = category_name
        category.save()
        messages.success(request, f'Category Updated Successfully!')
        return redirect('categories')

@login_required
def delete_category(request, id):
    category = get_object_or_404(Category, id = id)
    category.delete()
    messages.success(request, f'Category Deleted Successfully!')
    return redirect('categories')

# PRODUCTS
@login_required
def productsList(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    add_product_form = addProductForm(request.POST or None)

    template_name = 'main/products.html'
    context = {
        'products':products,
        'add_product_form': add_product_form,
        'categories':categories,
    }
    return render(request, template_name, context)

@login_required
def create_product(request):
    if request.method == "POST" and request.FILES:
        name = request.POST.get('name')
        description = request.POST.get('description')
        category = request.POST.get('category')
        price = int(request.POST.get('price'))
        discount_price = int(request.POST.get('discount_price'))
        still_instock = request.POST.get('still_instock')
        image1 = request.FILES['image1']


        if still_instock == "on":
            still_instock = True
        else:
            still_instock = False

        category_instance = get_object_or_404(Category, name = category)

        try:
            image2 = request.FILES['image2']
            image3 = request.FILES['image3']
            instance = Product (
                name = name,
                description = description,
                category = category_instance,
                price = price,
                discount_price = discount_price,
                still_instock = still_instock,
                image1 = image1,
                image2 = image2,
                image3 = image3,
            )
            instance.save()
            messages.success(request, f'Product Added Successfully!')
            return redirect('products')
        except:
            instance = Product (
                name = name,
                description = description,
                category = category_instance,
                price = price,
                discount_price = discount_price,
                still_instock = still_instock,
                image1 = image1,
            )
            instance.save()

            messages.success(request, f'Product Added Successfully!')
            return redirect('products')
    messages.warning(request, f'Error Occured while saving your data!')
    return redirect('products')

@login_required
def update_product(request, id):
    if request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('description')
        category = request.POST.get('category')
        price = int(request.POST.get('price'))
        discount_price = int(request.POST.get('discount_price'))
        still_instock = request.POST.get('still_instock')



        if still_instock == "on":
            still_instock = True
        else:
            still_instock = False

        category_instance = get_object_or_404(Category, name = category)

        product = Product.objects.get(id=id)
        product.name = name
        product.description = description
        product.category = category_instance
        product.price = price
        product.discount_price = discount_price
        product.still_instock = still_instock
        try:
            image1 = request.FILES['image1']
            product.image1 = image1
        except:
            pass
        try:
            image2 = request.FILES['image2']
            product.image2 = image2
        except:
            pass
        try:
            image3 = request.FILES['image3']
            product.image3 = image3
        except:
            pass
        product.save()
        messages.success(request, f'Product Updated Successfully!')
        return redirect('products')
    messages.warning(request, f'Error Occured while updating your data!')
    return redirect('products')

@login_required
def delete_product(request, id):
    product = get_object_or_404(Product, id = id)
    product.delete()
    messages.success(request, f'Product Deleted Successfully!')
    return redirect('products')

def make_order(request, id):
    form = messageForm(request.POST or None)
    product = get_object_or_404(Product, id = id)
    template_name = 'main/order.html'
    context = {
        'form': form,
        'product': product,
    }
    return render(request, template_name, context)


def order(request, id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id = id)
        form  = messageForm(request.POST or None)
        if form.is_valid():
            order = form.save(commit = False)
            order.product = product
            order.product_name = product.name
            order.save()

            customer_name = form.cleaned_data['name']
            header = customer_name + " - Is making an Order"

            message_from_customer = form.cleaned_data['message']
            email_from_customer = form.cleaned_data['email']
            phone_number_from_customer = form.cleaned_data['phone_number']

            users = CustomUser.objects.all()

            mail_list = [user.email for user in users]
            print(mail_list)

            message = message_from_customer + "\n" + "DETAILS OF THE PRODUCT"+ "\n" + "Product ordered: " + product.name + " \n" + "Product Description: "+ product.description + "\n" + "Sender's Email: " + email_from_customer + "\n" + "Sender's Phone number: " + phone_number_from_customer
            mail = EmailMessage(header, message, to=mail_list)
            mail.send(fail_silently = False)

            messages.success(request, f'Thank you for placing your order! We\'ll contact you soon.')
            return redirect('catalog')
    messages.warning(request, f'Error occured while placing an order. Please try again.')
    return redirect('make-order', product.id)


def message(request):
    if request.method == 'POST':
        form  = messageForm(request.POST or None)
        if form.is_valid():
            message = form.save(commit = False)
            message.is_order = False
            message.save()


            customer_name = form.cleaned_data['name']
            header = customer_name + " - Is messaging"

            message_from_customer = form.cleaned_data['message']
            email_from_customer = form.cleaned_data['email']
            phone_number_from_customer = form.cleaned_data['phone_number']

            message = message_from_customer + "\n" + "Sender's Email: "+ email_from_customer + "\n" + "Sender's Phone number: " + phone_number_from_customer
            mail = EmailMessage(header, message, to=["jonas@mail.test"])
            mail.send(fail_silently = False)

            messages.success(request, f'Thank you. Message has been delivered.')
            return redirect('home')
        else:
            print("Invalid form")
    return redirect('home')
