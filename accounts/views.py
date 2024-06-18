"""
This contains views for the accounts app.
"""

from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.contrib.sites import requests
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, View, DetailView

from accounts.forms import SignUpForm, SignInForm


class SignUpView(CreateView):
    """
    This view is used to sign up a user.
    """
    template_name = 'accounts/signup.html'
    form_class = SignUpForm

    def form_valid(self, form):
        """
        This function is used to validate the form
        and create the user account. If the form is
        valid it logs in the user.
        :param form:
        :return:
        """
        user = form.save()
        login(self.request, user)
        messages.success(self.request, 'Signup Successful')
        return redirect('customers:customer_dashboard')

    def form_invalid(self, form):
        """
        This function is used to validate the form
        if invalid, it returns the form with the error message.
        :param form:
        :return:
        """
        messages.error(self.request, "There was an error signing you up")
        return super().form_invalid(form)

    pass


class SignInView(View):
    template_name = 'accounts/signin.html'
    form_class = SignInForm

    def get(self, request):
        form = self.form_class()
        if request.user.is_authenticated:
            messages.info(self.request, 'You are already logged in.')
            return redirect('customers:customer_dashboard')
        return render(request, self.template_name, context={'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = authenticate(request, email=form.cleaned_data['email'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                messages.success(self.request, 'Login Successful')
                url = request.META.get('HTTP_REFERER')
                try:
                    query = requests.utils.urlparse(url).query
                    params = dict(x.split('=') for x in query.split('&'))
                    if 'next' in params:
                        next_page = params['next']
                        return redirect(next_page)
                finally:
                    pass
                    return redirect('customers:customer_dashboard')
            else:
                message = 'Your email or password is incorrect. Please try again.'
                return render(request, self.template_name, context={'form': form, 'message': message})


class ChangePasswordView(LoginRequiredMixin, PasswordChangeView):
    """
    This view is used to change the password.
    """
    template_name = 'accounts/password/password_change.html'
    success_url = reverse_lazy('accounts:customer_dashboard')

    def form_valid(self, form):
        """
        This function is used to validate the form
        :param form:
        :return:
        """
        messages.success(self.request, 'Your password has been changed successfully.')
        return super().form_valid(form)

    def form_invalid(self, form):
        """
        This function is used to check if the form is invalid
        :param form:
        :return:
        """
        messages.error(self.request, "There was an error changing your password. Please try again.")
        return super().form_invalid(form)
