"""
This holds url routes for all the pages in this application
"""
from django.urls import path
from . import views

app_name = 'pages'
urlpatterns = [
    path('landing/', views.IndexView.as_view(), name='home'),

    # path('landing/', views.LandingPageView.as_view(), name='landing_page'),

    path('app/', views.AppView.as_view(), name='app_home'),
]
