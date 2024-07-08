from django.contrib.auth.base_user import BaseUserManager

"""
Custom manager for user account creation using Django's BaseUserManager.
"""


class UserAccountManager(BaseUserManager):
    """
    Custom manager for user account creation.
    """

    def create_user(self, email: str, password: str = None, **kwargs):
        """
        Create and save a new user.

        Args:
            email (str): User's email address.
            password (str, optional): User's password.
            **kwargs: Additional user attributes.

        Returns:
            User: Created user instance.
        """
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        email = email.lower()
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email: str, password: str, **kwargs):
        """
        Create and save a new superuser.

        Args:
            email (str): Superuser's email address.
            password (str): Superuser's password.
            **kwargs: Additional user attributes.

        Returns:
            User: Created superuser instance.
        """
        user = self.create_user(email, password, **kwargs)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user
