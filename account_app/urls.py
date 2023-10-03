from django.urls import path
from . import views

app_name = 'account_app'
urlpatterns = [
    path('contact/', views.ContactUsView.as_view(), name='contact'),
    path('about/',views.AboutView.as_view(), name='about')
]