from flask_login import UserMixin
from mongoengine import DynamicDocument


class User(UserMixin, DynamicDocument):
    def authenticated(self, with_password=False, password=''):
        """
        Ensure a user is authenticated, and optionally check their password.

        :param with_password: Optionally check their passowd
        :type with_password: bool
        :param password: Optionally verify this as their password
        :type password: str
        :return: boolean
        """
        if with_password:
            return check_password_hash(self.password, password)
        return self.password == password
