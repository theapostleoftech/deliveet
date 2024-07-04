"""
This holds url routes for all the pages in this application
"""
from django.urls import path
from . import views

app_name = 'pages'
urlpatterns = [
    path('app/', views.IndexView.as_view(), name='home'),

    path('landing/', views.LandingPageView.as_view(), name='landing_page'),

    path('', views.HomeView.as_view(), name='app_home'),
]
