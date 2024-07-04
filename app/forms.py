"""
This contains base form for all the forms in deliveet
"""

from django import forms


# class BaseForm(forms.Form):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.setup_form_classes()
#
#     def setup_form_classes(self):
#         for field_name, field in self.fields.items():
#             # Customize label class
#             field.label_classes = 'block mb-2 text-sm font-medium text-gray-900 dark:text-white'
#
#             # Customize widget class
#             if isinstance(field.widget, (forms.TextInput, forms.EmailInput, forms.PasswordInput, forms.Textarea)):
#                 field.widget.attrs.update({
#                     'class': 'bg-gray-50 border border-gray-300 \
#                     text-gray-900 text-sm rounded-lg focus:ring-primary-600 \
#                     focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 \
#                     dark:border-gray-600 dark:placeholder-gray-400 dark:text-white \
#                     dark:focus:ring-blue-500 dark:focus:border-blue-500'
#                 })


class BaseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            # Add CSS classes to form fields
            field.widget.attrs[
                'class'] = 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 \
                focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 \
                dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'

            # Add CSS classes to form labels
            field.label_attrs = {
                'class': 'block mb-2 text-sm font-medium text-gray-900 dark:text-white'
            }

            # Add CSS classes to form placeholders
            field.widget.attrs['placeholder'] = 'form-placeholder'
            field.widget.attrs['placeholder_class'] = 'placeholder-gray-500 dark:placeholder-gray-400'

            # Add CSS classes to form help text
            field.help_text_attrs = {
                'class': 'mt-2 text-sm text-red-600 dark:text-red-500'
            }

            # Add CSS classes to form errors
            field.error_attributes = {
                'class': 'text-red-700 dark:text-red-500'
            }
