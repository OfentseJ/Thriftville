from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime
from .models import *
from .utils import cookieCart, cartData, guestOrder


def index(request):
     products = Product.objects.all()
     data = cartData(request)

     cartItems = data['cartItems']
     order = data['order']
     items = data['items']

     context = {'products': products, 'items':items, 'order':order, 'cartItems': cartItems}
     return render(request, 'store/index.html', context)

def login(request):
     context = {}
     return render(request, 'store/login.html', context)

def register(request):
     context = {}
     return render(request, 'store/register.html', context)


def checkout(request):

     data = cartData(request)

     cartItems = data['cartItems']
     order = data['order']
     items = data['items']

     context = {'items':items, 'order':order, 'cartItems': cartItems}
     return render(request, 'store/checkout.html', context)

def cart(request):
      
     data = cartData(request)

     cartItems = data['cartItems']
     order = data['order']
     items = data['items']

     context = {'items':items, 'order':order, 'cartItems': cartItems}
     return render(request, 'store/cart.html', context)

def shop(request):
     products = Product.objects.all()
     data = cartData(request)

     cartItems = data['cartItems']
     order = data['order']
     items = data['items']
          
     context = {'products': products, 'items':items, 'order':order, 'cartItems': cartItems}
     return render(request, 'store/shop.html', context)

def updateItem(request):
     data = json.loads(request.body)
     productId = data['productId']
     action = data['action']

     print('action:', action)
     print('productId:', productId)

     customer = request.user.customer
     product = Product.objects.get(id=productId)
     order, created = Order.objects.get_or_create(customer=customer, complete=False)
     
     orderItem ,created = OrderItem.objects.get_or_create(order=order, product=product)
     
     if action == 'add':
          message = 'Item was added'
     elif action == 'remove':
          orderItem.quantity = (orderItem.quantity - 1)
     
     orderItem.save()

     if orderItem.quantity <= 0:
          orderItem.delete()
          message = 'Item was removed'

     return JsonResponse(message, safe=False)

def processOrder(request):
     transaction_id = datetime.datetime.now().timestamp
     data = json.loads(request.body)


     if request.user.is_authenticated:
          customer = request.user.customer
          order, created = Order.objects.get_or_create(customer=customer, complete=False)

     else:
          customer, order = guestOrder(request,data)
     
     total = float(data['form']['total'])
     order.transection_id = transaction_id

     if total == order.get_cart_total:
          order.complete = True

     order.save()

     ShippingAddress.objects.create(
          customer = customer,
          order=order,
          address=data['shipping']['address'],
          city=data['shipping']['city'],
          province=data['shipping']['province'],
          zipcode=data['shipping']['zipcode'],
     )

     return JsonResponse('Payment complete', safe=False)