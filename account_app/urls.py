from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views

app_name = 'account_app'
urlpatterns = [
    path('contact/', views.ContactUsView.as_view(), name='contact'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('otp/', views.CheckOtpView.as_view(), name='check_otp'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('verify/email/', views.VerifyEmailView.as_view(), name='verify_email'),
    path('change/password/<token>/', views.ChangePasswordView.as_view(), name='change_password'),

]
