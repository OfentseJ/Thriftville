from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime
from .models import *
from .utils import cookieCart, cartData, guestOrder
from django.http import JsonResponse
import json
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import Customer
from .serializers import CustomerRegistrationSerializer, UserLoginSerializer
from django.views.generic import TemplateView
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import *
from django.urls import reverse_lazy
from rest_framework.views import APIView
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponse
from .forms import EditAccountForm


def index(request):
     products = Product.objects.all()
     data = cartData(request)

     cartItems = data['cartItems']
     order = data['order']
     items = data['items']

     context = {'products': products, 'items':items, 'order':order, 'cartItems': cartItems}
     return render(request, 'store/index.html', context)

def user_login(request):
    template_name = 'login.html'
    error = None 
    errors = None  
    
    if request.method == 'POST':
        serializer = UserLoginSerializer(data=request.POST)
        if serializer.is_valid():
            user = authenticate(email=serializer.validated_data['email'], password=serializer.validated_data['password'])
            if user:
                login(request, user)
                if user.is_staff:
                    return redirect('admin:index')
                else:
                    return redirect('index')
            else:
                error = 'Invalid email or password'
        else:
            errors = serializer.errors
    else:
        serializer = UserLoginSerializer() 

    return render(request, template_name, {'form': serializer, 'error': error, 'errors': errors})

class CustomerRegistrationView(TemplateView):
    template_name = 'register.html'

    def post(self, request, *args, **kwargs):
        serializer = CustomerRegistrationSerializer(data=request.POST)
        if serializer.is_valid():
            serializer.save()
            
            return HttpResponseRedirect(reverse_lazy('index'))  
        else:
            
            return render(request, self.template_name, {'serializer': serializer})

def aboutUs(request):
     data = cartData(request)

     cartItems = data['cartItems']
     order = data['order']
     items = data['items']

     context = {'items':items, 'order':order, 'cartItems': cartItems}
     return render(request, 'store/about_us.html', context)

def contact(request):
     data = cartData(request)

     cartItems = data['cartItems']
     order = data['order']
     items = data['items']

     context = {'items':items, 'order':order, 'cartItems': cartItems}
     return render(request, 'store/contact.html', context)


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

def profile(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items':items, 'order':order, 'cartItems': cartItems}
    return render(request, 'store/profile.html', context)

def logout_view(request):
    logout(request)
    return redirect('index')
    
@login_required
@api_view(['GET'])
def account_page_view(request):
    
    account_info = {
        'username': request.user.username,
        'email': request.user.email,
    }
    return Response(account_info)

@login_required
def edit_account_view(request):

    if request.method == 'POST':
        form = EditAccountForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = EditAccountForm(instance=request.user)
    return render(request, 'store/edit_account.html', {'form': form})

def track_order_view(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items':items, 'order':order, 'cartItems': cartItems}

    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items':items, 'order':order, 'cartItems': cartItems}

    confirmed_orders = Order.objects.filter(customer__user=request.user, complete=True)

    
    if confirmed_orders.exists():
        return render(request, 'store/track_order.html', {'confirmed_orders': confirmed_orders},context)
    else:
        
        message = "You don't have any confirmed orders at the moment."
        return render(request, 'store/track_order.html', {'message': message},context)
    

def log_return_exchange(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items':items, 'order':order, 'cartItems': cartItems}


    if request.method == 'POST':
        item_quality = request.POST.get('item_quality', '')
        item_price = request.POST.get('item_price', '')
        
        email = request.POST.get('email', '')

        
        subject = 'Return/Exchange Request'
        message = f'Item Quality: {item_quality}\nItem Price: {item_price}\nEmail: {email}'
        sender_email = 'thriftville.inbox@gmail.com'  
        recipient_email = 'thriftville.inbox@gmail.com'
        send_mail(subject, message, sender_email, [recipient_email])

        return HttpResponse('Return/Exchange request sent successfully!')
    else:
        return render(request, 'store/log_return_exchange.html', context)
 
def help_center(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items':items, 'order':order, 'cartItems': cartItems}


    if request.method == 'POST':
       
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        
        subject = f"Message from {name}"
        email_message = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"

       
        send_mail(
            subject,
            email_message,
            'thriftville.inbox@gmail.com',  
            ['thriftville.inbox@gmail.com'], 
            fail_silently=False,
        )
       

    return render(request, 'store/help_center.html',context)