from django.urls import path

from . import views

urlpatterns = [
        #Leave as empty string for base url
	path('', views.index, name="index"),
	path('login/', views.login, name="login"),
    path('register/', views.register, name="register"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
	path('shop/', views.shop, name="shop"),
    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="processOrder")
]