"""
This contains url routes for the accounts app.
"""
from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('signin/', views.SignInView.as_view(), name='signin'),
    path('signout/', LogoutView.as_view(), name='signout'),

]
