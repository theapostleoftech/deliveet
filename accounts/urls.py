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
    path('me/', views.UserAccountDetailView.as_view(), name='user_account_details'),
    path('settings/', views.UserAccountUpdateView.as_view(), name='user_settings'),
    path('reset-password/', views.ResetPasswordView.as_view(), name='reset_password'),
    path('reset-password/done/', views.ResetPasswordDoneView.as_view(), name='reset_password_done'),
    path('reset/<uidb64>/<token>/', views.ResetPasswordConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.ResetPasswordCompleteView.as_view(), name='password_reset_complete'),

    # path('update/phone/', views.UpdatePhoneNumberView.as_view(), name='verify_update_phone'),

]
