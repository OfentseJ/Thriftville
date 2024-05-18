from django.urls import path
from django.urls import path
from .views import CustomerRegistrationView
from . import views
from django.contrib.auth import views as auth_views


from . import views

urlpatterns = [
        #Leave as empty string for base url
	path('', views.index, name="index"),
	path('login/', views.user_login, name="login"),
    path('register/', views.CustomerRegistrationView.as_view(), name="register"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
	path('shop/', views.shop, name="shop"),
    path('about_us/', views.aboutUs, name="aboutUs"),
    path('contact/', views.contact, name="contact"),
    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="processOrder"),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout_view, name='logout'),
    path('account/', views.account_page_view, name='account_page'),
    path('account/edit/', views.edit_account_view, name='edit_account'),
    path('track_order/', views.track_order_view, name='track_order'),
    path('log_return_exchange/', views.log_return_exchange, name='log_return_exchange'),
    path('help-center/', views.help_center, name='help_center'),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="reset_password.html"), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="password_reset_done.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_confirm.html"), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_complete.html"), name="password_reset_complete"),
]