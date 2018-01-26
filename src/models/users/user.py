import uuid

from src.common.database import Database
from src.common.utils import Utils

import src.models.users.errors as UserErrors
from src.models.alerts.alert import Alert
import src.models.users.constants as UserConstants


class User(object):
    def __init__(self, email, password, _id=None):
        self.email = email
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<User {}>".format(self.email)

    @staticmethod
    def register_user(email, password):
        user_data = Database.find_one(UserConstants.COLLECTION, {"email": email})

        if user_data is not None:
            raise UserErrors.UserAlreadyRegisteredError("The email that was used is already registered.")
        if not Utils.email_is_valid(email):
            raise UserErrors.InvalidEmailError("Invalid email format.")

        User(email, Utils.hash_password(password)).save_to_db()

        return True

    def get_alerts(self):
        return Alert.find_by_user_email(self.email)

    def save_to_db(self):
        Database.insert(UserConstants.COLLECTION, self.json())

    def json(self):
        return {
            "_id": self._id,
            "email": self.email,
            "password": self.password
        }

    @staticmethod
    def login_is_valid(email, password):
        """
        This method verifies that an email password combo is valid or not. It checks that the email
        exists and that the password matches.
        :param email: The user's email
        :param password: The user's hashed password
        :return: True if valid otherwise False
        """

        user_data = Database.find_one(UserConstants.COLLECTION, {"email": email})
        if user_data is None:
            raise UserErrors.UserNotExistsError("The specified user doesn't exist.")
        if not Utils.check_hashed_password(password, user_data['password']):
            raise UserErrors.IncorrectPasswordError("The password is incorrect.")

        return True

    @classmethod
    def get_from_email(cls, email):
        return cls(**Database.find_one(UserConstants.COLLECTION, {"email": email}))
