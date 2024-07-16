"""
This contains views for the accounts app.
"""
import firebase_admin
from django.contrib import messages
from django.contrib.auth import login, authenticate, get_user_model, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordResetDoneView, PasswordResetView, \
    PasswordResetCompleteView, PasswordResetConfirmView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sites import requests
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, View, DetailView, FormView
from firebase_admin import auth, credentials

from accounts.forms import SignUpForm, SignInForm, ChangePasswordForm, UserAccountUpdateForm
from accounts.models import UserAccount
from deliveet.settings import FIREBASE_SECRETS

UserModel = get_user_model()

try:
    cred = credentials.Certificate(FIREBASE_SECRETS)
    firebase_admin.initialize_app(cred)
except ValueError as e:
    raise ValueError("Failed to initialize Firebase credentials: {}".format(e))


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
        """
        user = form.save()
        login(self.request, user)
        messages.success(self.request, 'Signup Successful')

        if user.account_type == UserAccount.UserAccountType.COURIER:
            return redirect('couriers:courier_dashboard')
        else:
            return redirect('customers:customer_dashboard')

    def form_invalid(self, form):
        """
        If the form is invalid, add error messages and redisplay the form.
        """
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}")
        return super().form_invalid(form)

    pass


class SignInView(View):
    template_name = 'accounts/signin.html'
    form_class = SignInForm

    def get(self, request):
        form = self.form_class()
        if request.user.is_authenticated and request.user.is_customer:
            messages.info(self.request, 'You are already logged in.')
            return redirect('customers:customer_dashboard')
        elif request.user.is_authenticated and request.user.is_courier:
            messages.info(self.request, 'You are already logged in.')
            return redirect('couriers:courier_dashboard')
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


class UserAccountDetailView(LoginRequiredMixin, DetailView):
    """
    This view displays the details of the user account.
    """
    model = UserModel
    template_name = 'accounts/user_account_details.html'
    context_object_name = 'user_account'

    def get_object(self, queryset=None):
        """
        This function returns the user account
        object for the currently logged-in user.
        """
        return self.request.user


@method_decorator([login_required], name='dispatch')
class UserAccountUpdateView(FormView):
    """
    This view updates the user account records
    It updates the user password and the user details
    """
    template_name = 'accounts/update_user_account.html'
    success_url = reverse_lazy('customers:customer_dashboard')

    def get(self, request, *args, **kwargs):
        user_form = UserAccountUpdateForm(instance=request.user)
        password_form = ChangePasswordForm(request.user)
        return render(request, self.template_name, {
            'user_form': user_form,
            'password_form': password_form
        })

    def post(self, request, *args, **kwargs):
        if request.POST.get('action') == 'update_user_details':
            user_form = UserAccountUpdateForm(request.POST, instance=request.user)
            if user_form.is_valid():
                user_form.save()
                if request.user.account_type == 'customer':
                    messages.success(request, 'Your profile has been updated')
                    return redirect(reverse('customers:customer_dashboard'))
                else:
                    messages.success(request, 'Your profile has been updated')
                    return redirect(reverse('couriers:courier_dashboard'))

        elif request.POST.get('action') == 'update_user_password':
            password_form = ChangePasswordForm(request.user, request.POST)
            if password_form.is_valid():
                password_form.save()
                update_session_auth_hash(request, password_form.user)
                if request.user.account_type == 'customer':
                    messages.success(request, 'Your profile has been updated')
                    return redirect(reverse('customers:customer_dashboard'))
                else:
                    messages.success(request, 'Your profile has been updated')
                    return redirect(reverse('couriers:courier_dashboard'))
        elif request.POST.get('action') == 'update_user_phone':
            firebase_user = auth.verify_id_token(request.POST.get('id_token'))

            request.user.phone_number = firebase_user['phone_number']
            if request.user.phone_number:
                request.user.phone_number_verified = True
                request.user.save()
                if request.user.account_type == 'customer':
                    messages.success(request, 'Your phone has been updated')
                    return redirect(reverse('customers:customer_dashboard'))
                else:
                    messages.success(request, 'Your profile has been updated')
                    return redirect(reverse('couriers:courier_dashboard'))
            else:
                messages.error(request, 'Your phone number has not been verified')


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    """
    This view resets the password.
    It inherits PasswordResetView
    """
    template_name = 'accounts/password/password_reset.html'
    form_class = PasswordResetForm
    email_template_name = 'registration/password_reset_email.html'
    subject_template_name = 'registration/password_reset_subject.txt'
    success_url = reverse_lazy('accounts:reset_password_done')

    pass


class ResetPasswordDoneView(PasswordResetDoneView):
    """
    This view serves the form for resetting the password
    It inherits PasswordResetDoneView
    """
    template_name = 'accounts/password/password_reset_done_view.html'
    pass


class ResetPasswordConfirmView(PasswordResetConfirmView):
    """
    This view is responsible for the password reset url.
    It inherits PasswordResetConfirmView
    """
    template_name = 'accounts/password/password_reset_confirm_view.html'
    success_url = reverse_lazy('accounts:password_reset_complete')


class ResetPasswordCompleteView(SuccessMessageMixin, PasswordResetCompleteView):
    """
    This view shows the password reset complete page.
    It inherits PasswordResetCompleteView
    """
    template_name = 'accounts/password/password_reset_complete_view.html'
    pass
