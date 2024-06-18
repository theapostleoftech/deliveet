"""
This contains url routes for the accounts app.
"""
from django.contrib.auth.views import LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView
from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('signin/', views.SignInView.as_view(), name='signin'),
    path('signout/', LogoutView.as_view(), name='signout'),
    path('reset-password/', PasswordResetView.as_view(template_name='accounts/password/password_reset.html'), name='reset_password'),
    path('reset-password/done/', PasswordResetDoneView.as_view(
        template_name='accounts/password/password_reset_done_view.html'
    ), name='reset_password_done'),

    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        template_name='accounts/password/password_reset_confirm_view.html'
    ), name='password_reset_confirm'
         ),

    path('reset/done/', PasswordResetCompleteView.as_view(
        template_name='accounts/password/password_reset_complete_view.html'
    ), name='password_reset_complete'
         ),

]
