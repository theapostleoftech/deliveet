from django.contrib.auth.base_user import BaseUserManager


class UserAccountManager(BaseUserManager):
    """
    This is the manager class that
    handles all account creation in the database
    """
    use_in_migrations = True

    def create_user(self, email, password=None, **kwargs):
        """
        Creates and saves a new user
        """
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        email = email.lower()
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **kwargs):
        """
        Creates and saves a new superuser
        """
        user = self.create_user(email, password, **kwargs)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

    pass
