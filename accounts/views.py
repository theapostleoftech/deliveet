"""
This contains views for the accounts app.
"""

from django.contrib import messages
from django.contrib.auth import login, authenticate, get_user_model, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView, PasswordResetDoneView, PasswordResetView, \
    PasswordResetCompleteView, PasswordResetConfirmView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sites import requests
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, View, DetailView, UpdateView, FormView

from accounts.forms import SignUpForm, SignInForm, ChangePasswordForm, UserAccountUpdateForm
from accounts.models import UserAccount

UserModel = get_user_model()


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
    success_url = reverse_lazy('customers:customer_dashboard')

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


# class UserAccountUpdateView(LoginRequiredMixin, UpdateView):
#     """
#     This view is used to update the user account.
#     """
#     model = UserModel
#     fields = ['first_name', 'last_name', 'email']
#     template_name = 'accounts/update_user_account.html'
#     success_url = reverse_lazy('customers:customer_dashboard')
#     success_message = 'Your profile has been updated successfully.'
#
#     def get_object(self, queryset=None):
#         """
#         This function returns the user account object
#         for the currently logged-in user.
#         """
#         return self.request.user

#
# class ChangePasswordViews(LoginRequiredMixin, FormView):
#     template_name = 'accounts/password/password_change.html'
#     form_class = ChangePasswordForm
#     success_url = reverse_lazy('accounts:password_change_done')
#
#     def get_form_kwargs(self):
#         kwargs = super().get_form_kwargs()
#         kwargs['user'] = self.request.user
#         return kwargs
#
#     def form_valid(self, form):
#         user = self.request.user
#         new_password = form.cleaned_data['new_password']
#         user.set_password(new_password)
#         user.save()
#         update_session_auth_hash(self.request, user)
#         messages.success(self.request, 'Your password has been changed successfully.')
#         return super().form_valid(form)
#
#     def form_invalid(self, form):
#         messages.error(self.request, 'There was an error changing your password. Please try again.')
#         return super().form_invalid(form)
#
#
# class UserAccountUpdateView(LoginRequiredMixin, FormView):
#     """
#     This view updates the user account records
#     It updates the user password and the user details
#     """
#     template_name = 'accounts/update_user_account.html'
#     form_class = None
#     success_url = reverse_lazy('customers:customer_dashboard')
#
#     def get_form_class(self):
#         """
#         This function retrieves the various forms for the user account.
#         :return:
#         """
#         if self.request.POST.get('action') == 'update_user_details':
#             return UserAccountUpdateForm
#         elif self.request.POST.get('action') == 'update_user_password':
#             return ChangePasswordForm
#         return None
#
#     def get_form_kwargs(self):
#         kwargs = super().get_form_kwargs()
#         form_class = self.get_form_class()
#
#         if form_class is None:
#             return kwargs
#
#         if self.request.POST.get('action') == 'update_user_details':
#             kwargs['instance'] = {
#                 'user_form': self.request.user,
#                 # 'customer_form': self.request.user.customer,
#             }
#         elif self.request.POST.get('action') == 'update_user_password':
#             kwargs['user'] = self.request.user
#         return kwargs
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['user_form'] = UserAccountUpdateForm(instance=self.request.user)
#         # context['customer_form'] = BasicCustomerForm(instance=self.request.user.customer)
#         context['password_form'] = ChangePasswordForm(self.request.user)
#         return context
#
#     def form_valid(self, form):
#         if self.request.POST.get('action') == 'update_user_details':
#             user_form = form[0]
#             customer_form = form[1]
#             user_form.save()
#             customer_form.save()
#             messages.success(self.request, 'Your profile has been updated')
#         elif self.request.POST.get('action') == 'update_user_password':
#             user = form.save()
#             update_session_auth_hash(self.request, user)
#             messages.success(self.request, 'Your password has been updated')
#         elif self.request.method == 'GET':
#             return UserAccountUpdateForm
#             pass
#         # elif self.request.POST.get('action') == 'update_phone':
#         #     # Get Firebase user data
#         #     firebase_user = auth.verify_id_token(self.request.POST.get('id_token'))
#         #     self.request.user.customer.phone_number = firebase_user['phone_number']
#         #     self.request.user.customer.save()
#         return super().form_valid(form)
#
#     def post(self, request, *args, **kwargs):
#         self.object = None
#         form_class = self.get_form_class()
#         form_kwargs = self.get_form_kwargs()
#         if form_class:
#             if isinstance(form_class, tuple):
#                 form = [form_class[0](**form_kwargs['instance']), form_class[1](**form_kwargs['instance'])]
#             else:
#                 form = form_class(**form_kwargs)
#             if form.is_valid():
#                 return self.form_valid(form)
#         return self.form_invalid(form)


class UserAccountUpdateView(LoginRequiredMixin, FormView):
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
                messages.success(request, 'Your profile has been updated')
                return redirect(self.success_url)
        elif request.POST.get('action') == 'update_user_password':
            password_form = ChangePasswordForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Your password has been updated')
                return redirect(self.success_url)
        return redirect(self.success_url)


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
