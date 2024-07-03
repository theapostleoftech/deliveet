"""
This holds url routes for all the pages in this application
"""
from django.urls import path
from . import views

app_name = 'pages'
urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),
    path('sample', views.SampleView.as_view(), name='sample'),

    path('landing/', views.SampleView.as_view(), name='landing_page'),
]
