from os import name
from django import forms
from django.contrib.messages.api import success
from django.db.models.query import QuerySet
from django.shortcuts import render,redirect
from django.http import HttpResponse
from bookstore.decorators import notLoggedUser

from bookstore.forms import CreateNewUser,CustomerForm

from .models import *
from .forms import OrderForm,CreateNewUser,CustomerForm
from .filters import OrderFilter
from django.forms import inlineformset_factory
from  django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,logout
from django.contrib.auth import login as myLogin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .decorators import notLoggedUser,allowedUsers,forAdmins

import requests
from django.conf import settings
# from .forms import ModelForm
# Create your views here.

@login_required(login_url='login')
# @allowedUsers(allowedGroups=['admin'])
@forAdmins
def home(request):
    customers = Customer.objects.all()
    orders = Order.objects.all()
    t_orders = orders.count()
    p_orders = orders.filter(status='Pending').count()
    d_orders = orders.filter(status='Delivered').count()
    in_orders = orders.filter(status='in Progress').count()
    out_orders = orders.filter(status='Out of Oreder').count()
    context = { 'customers': customers,
                'orders': orders, 
                't_orders': t_orders,
                'p_orders': p_orders, 
                'd_orders': d_orders, 
                'in_orders': in_orders,
                'out_orders': out_orders}
    return render(request, 'bookstore/dashboard.html', context)

@login_required(login_url='login')
@forAdmins
def books(request):
    books = Book.objects.all()
    return render(request, 'bookstore/books.html', {'books': books})

@login_required(login_url='login')
def customer(request,pk):
    customer= Customer.objects.get(id=pk)

    orders = customer.order_set.all()
    number_orders = orders.count() 
    searchFilter = OrderFilter(request.GET,queryset=orders)
    orders= searchFilter.qs
    context = { 'customer': customer,'myFilter':searchFilter,'orders': orders,'number_orders':number_orders }
    return render(request, 'bookstore/customer.html',context)



# def create(request):
#     form = OrderForm()
#     if request.method == 'POST':
#         # print(request.POST)
#         form = OrderForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('/')
#     context = {'form': form}
#     return render(request, 'bookstore/my_order_form.html', context)

@login_required(login_url='login')
@allowedUsers(allowedGroups=['admin'])
def create(request,pk):
    OrderFormSet = inlineformset_factory(Customer,Order,fields=('book','status'),extra=8)
    customer= Customer.objects.get(id = pk)
    # form = OrderForm()
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    if request.method == 'POST':
        # print(request.POST)
        # form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST,instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')
    # context = {'form': form}
    context = {'formset': formset}
    return render(request, 'bookstore/my_order_form.html', context)


@login_required(login_url='login')
@allowedUsers(allowedGroups=['admin'])
def update(request,pk):
    order= Order.objects.get(id = pk)
    form = OrderForm(instance=order)
    if request.method == 'POST':
      
        form = OrderForm(request.POST,instance=order)
        if form.is_valid():
            form.save()
           
            return redirect('/')
    context = {'form': form}
    return render(request, 'bookstore/my_order_form.html', context)

@login_required(login_url='login')    
@allowedUsers(allowedGroups=['admin'])
def delete(request,pk):
    order= Order.objects.get(id = pk)
    if request.method == 'POST':
        order.delete()   
        return redirect('/')
    context = {'order': order}
    return render(request, 'bookstore/delete_form.html', context)




# def login(request):
   

#     context = {}
#     return render(request, 'bookstore/login.html', context)

@notLoggedUser
def register(request):
    form = CreateNewUser()
 
    if request.method=='POST':
        form=CreateNewUser(request.POST)
        if form.is_valid():
            recaptcha_response=request.POST.get('g-recaptcha-response')
            data= {
                'secret':settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response':recaptcha_response
            }
            r= requests.post('https://www.google.com/recaptcha/api/siteverify',data=data)
            result = r.json()
            if result['success']:
                user= form.save()
                username =form.cleaned_data.get('username')
                messages.success(request,username + 'created successfully')
                return redirect('login')
            else:
                messages.error(request, 'invalid recaptcha please try again')
     
            
    context = {'form':form}
    return render(request, 'bookstore/register.html', context)

@notLoggedUser
def login(request):
 
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        if user is not None:
            myLogin(request,user)
            return redirect('home')
        else:
            messages.info(request,'credintial error')
    context = {}
    return render(request, 'bookstore/login.html', context)

    
def userlogout(request):
   logout(request)
   return redirect('login')
    
@login_required(login_url='login')    
@allowedUsers(allowedGroups=['customer'])
def userProfile(request):
    # customer= Customer.objects.get(id=pk)

    orders = request.user.customer.order_set.all()
    t_orders = orders.count()
    p_orders = orders.filter(status='Pending').count()
    d_orders = orders.filter(status='Delivered').count()
    in_orders = orders.filter(status='in Progress').count()
    out_orders = orders.filter(status='Out of Oreder').count()
    context = { 'orders': orders, 
                't_orders': t_orders,
                'p_orders': p_orders, 
                'd_orders': d_orders, 
                'in_orders': in_orders,
                'out_orders': out_orders}

    return render(request, 'bookstore/profile.html', context)


@login_required(login_url='login')    
def profileInfo(request):
    customer=request.user.customer
    form=CustomerForm(instance=customer)
    if request.method == 'POST':
        form= CustomerForm(request.POST,request.FILES,instance=customer)
        if form.is_valid():
            form.save()

    context = {'form':form }

    return render(request, 'bookstore/profile_info.html', context)