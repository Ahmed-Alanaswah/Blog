from django.shortcuts import render
from django.http import HttpResponse
from .models import *
# Create your views here.


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


def books(request):
    books = Book.objects.all()
    return render(request, 'bookstore/books.html', {'books': books})


def customer(request,pk):
    customer= Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    number_orders = orders.count() 
    context = { 'customer': customer,'orders': orders,'number_orders':number_orders }
    return render(request, 'bookstore/customer.html',context)
