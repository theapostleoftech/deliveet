"""
This contains views for the accounts app.
"""
from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import redirect
from django.views.generic import CreateView

from accounts.forms import SignUpForm


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
        valid it logs in in the user.
        :param form:
        :return:
        """
        user = form.save()
        login(self.request, user)
        messages.success(self.request, 'Signup Successful')
        return redirect('')

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
