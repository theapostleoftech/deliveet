"""
This contains all the url routes for the finance app.
"""
from django.urls import path

from finance import views

app_name = 'finance'
urlpatterns = [
    path('wallet/', views.WalletView.as_view(), name='wallet'),
    path('transaction/', views.initiate_transaction, name='initiate_transaction'),
    path('verify-transaction/<str:transaction_reference>/', views.verify_transaction, name='verify_payment'),
]
