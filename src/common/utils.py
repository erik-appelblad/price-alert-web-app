from passlib.hash import pbkdf2_sha512
import re


class Utils(object):

    @staticmethod
    def email_is_valid(email):
        pattern = "^[\w-]+@([\w-]+\.)+[\w]+$"
        email_address_matcher = re.compile(pattern)
        return True if email_address_matcher.match(email) else False


    @staticmethod
    def hash_password(password):
        """
        Hashes a password using pbkdf2_sha512
        :param password: A password in sha512 hash from login/register form
        :return: A sha512 -> pbkdf2_sha512 encrypted password
        """
        
        return pbkdf2_sha512.encrypt(password)

    @staticmethod
    def check_hashed_password(password, hashed_password):
        """
        Checks that the user passed password matches the hashed password in the database.
        :param password: sha512-hashed password
        :param hashed_password: pbkdf2-sha512 encrypted password
        :return: True if they match, otherwise False
        """

        return pbkdf2_sha512.verify(password, hashed_password)