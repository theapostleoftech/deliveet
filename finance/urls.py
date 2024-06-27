"""
This contains all the url routes for the finance app.
"""
from django.urls import path

from finance import views

app_name = 'finance'
urlpatterns = [
    path('wallet/', views.WalletView.as_view(), name='wallet'),
    path('transaction/', views.initiate_transaction, name='initiate_transaction'),
    # path('verify-payment/<str:ref>/', views.verify_payment, name='verify_payment'),
]
