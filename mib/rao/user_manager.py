import json
from flask.globals import current_app, request
from mib.auth.user import User
from mib import app
from flask_login import (logout_user, current_user)
from flask import abort
import requests


class UserManager:
    USERS_ENDPOINT = app.config['USERS_MS_URL']
    REQUESTS_TIMEOUT_SECONDS = app.config['REQUESTS_TIMEOUT_SECONDS']

    @classmethod
    def get_user_by_id(cls, user_id: int) -> User:
        """
        This method contacts the users microservice
        and retrieves the user object by user id.
        :param user_id: the user id
        :return: User obj with id=user_id
        """
        try:
            response = requests.get("%s/users/%s" % (cls.USERS_ENDPOINT, str(user_id)),
                                    timeout=cls.REQUESTS_TIMEOUT_SECONDS)
            json_payload = response.json()
            if response.status_code == 200:
                # user is authenticated
                user = User.build_from_json(json_payload)
                
            else:
                raise RuntimeError(
                    'Server has sent an unrecognized status code %s' % response.status_code)

        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
            print(e)
            return abort(500)

        return user

    @classmethod
    def get_user_by_email(cls, user_email: str):
        """
        This method contacts the users microservice
        and retrieves the user object by user email.
        :param user_email: the user email
        :return: User obj with email=user_email
        """
        try:
            response = requests.get("%s/user_email/%s" % (cls.USERS_ENDPOINT, user_email),
                                    timeout=cls.REQUESTS_TIMEOUT_SECONDS)
            
            json_payload = response.json()
            user = None

            if response.status_code == 200:
                user = User.build_from_json(json_payload)

        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            return abort(500)

        return user

    @classmethod
    def get_user_by_phone(cls, user_phone: str) -> User:
        """
        This method contacts the users microservice
        and retrieves the user object by user phone.
        :param user_phone: the user phone
        :return: User obj with phone=user_phone
        """
        try:
            response = requests.get("%s/user_phone/%s" % (cls.USERS_ENDPOINT, user_phone),
                                    timeout=cls.REQUESTS_TIMEOUT_SECONDS)
            json_payload = response.json()
            user = None

            if response.status_code == 200:
                user = User.build_from_json(json_payload)

        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            return abort(500)

        return user

    @classmethod
    def create_user(cls,
                    email: str, password: str,
                    firstname: str, lastname: str,
                    birthdate):
        try:
            url = "%s/users" % cls.USERS_ENDPOINT
            response = requests.post(url,
                                     json={
                                         'email': email,
                                         'password': password,
                                         'firstname': firstname,
                                         'lastname': lastname,
                                         'birthdate': birthdate,
                                     },
                                     timeout=cls.REQUESTS_TIMEOUT_SECONDS
                                     )

        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            return abort(500)

        return response

    @classmethod
    def update_user(cls, user_id: int, email: str, firstname: str, lastname: str,
                    password: str, birthdate: str):
        """
        This method contacts the users microservice
        to allow the users to update their profiles
        :param phone:
        :param password:
        :param email:
        :param user_id: the customer id
            email: the user email
            password: the user password
            phone: the user phone
        :return: User updated
        """
        try:
            url = "%s/users/%s" % (cls.USERS_ENDPOINT, str(user_id))
            response = requests.put(url,
                                    json={
                                        'email': email,
                                        'password': password,
                                        'firstname': firstname,
                                        'lastname': lastname,
                                        'birthdate': birthdate,
                                    },
                                    timeout=cls.REQUESTS_TIMEOUT_SECONDS
                                    )
            return response

        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            return abort(500)

        raise RuntimeError('Error with searching for the user %s' % user_id)

    @classmethod
    def delete_user(cls, user_id: int):
        """
        This method contacts the users microservice
        to delete the account of the user
        :param user_id: the user id
        :return: User updated
        """
        try:
            logout_user()
            url = "%s/users/%s" % (cls.USERS_ENDPOINT, str(user_id))
            response = requests.delete(
                url, timeout=cls.REQUESTS_TIMEOUT_SECONDS)

        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            return abort(500)

        return response

    @classmethod
    def authenticate_user(cls, email: str, password: str) -> User:
        """
        This method authenticates the user trough users AP
        :param email: user email
        :param password: user password
        :return: None if credentials are not correct, User instance if credentials are correct.
        """
        payload = dict(email=email, password=password)
        try:
            
            response = requests.post('%s/authenticate' % cls.USERS_ENDPOINT,
                                     json=payload,
                                     timeout=cls.REQUESTS_TIMEOUT_SECONDS
                                     )
            
            json_response = response.json()
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            # We can't connect to Users MS
            return abort(500)

        if response.status_code == 401:
            # user is not authenticated
            return None
        elif response.status_code == 200:
            user = User.build_from_json(json_response['user'])
            return user
        else:
            raise RuntimeError(
                'Microservice users returned an invalid status code %s, and message %s'
                % (response.status_code, json_response['error_message'])
            )

    @classmethod
    def get_all_users(cls):
        try:
            url = "%s/users" % (cls.USERS_ENDPOINT)

            response = requests.get(url, timeout=cls.REQUESTS_TIMEOUT_SECONDS)
            json_payload = response.json()
            users = None

            if response.status_code == 200:
                users = json_payload

        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            return abort(500)

        return users

    @classmethod
    def add_user_to_blacklist(cls, id_blacklisted: int):
        try:
            url = "%s/users/%s/blacklist" % (cls.USERS_ENDPOINT,
                                             current_user.id)
            response = requests.post(url,
                                     json={
                                         'id': id_blacklisted
                                     },
                                     timeout=cls.REQUESTS_TIMEOUT_SECONDS
                                     )

        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            return abort(500)

        return response

    @classmethod
    def remove_user_from_blacklist(cls, id_blacklisted: int):
        try:
            url = "%s/users/%s/blacklist/%s" % (cls.USERS_ENDPOINT,
                                                current_user.id, id_blacklisted)
            response = requests.delete(
                url, timeout=cls.REQUESTS_TIMEOUT_SECONDS)

        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            return abort(500)

        return response

    @classmethod
    def get_blacklist(cls, id_user: int):
        try:
            url = "%s/users/%s/blacklist" % (cls.USERS_ENDPOINT,
                                             id_user)

            response = requests.get(url, timeout=cls.REQUESTS_TIMEOUT_SECONDS)
            json_payload = response.json()
            blacklist = None

            if response.status_code == 200:
                blacklist = json_payload

        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            return abort(500)

        return blacklist

    @classmethod
    def add_user_to_report(cls, id_reported: int):
        try:
            url = "%s/users/%s/report" % (cls.USERS_ENDPOINT,
                                          current_user.id)
            response = requests.post(url,
                                     json={
                                         'id': id_reported
                                     },
                                     timeout=cls.REQUESTS_TIMEOUT_SECONDS
                                     )

        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            return abort(500)

        return response

    @classmethod
    def get_report(cls, id_user: int):
        try:
            url = "%s/users/%s/report" % (cls.USERS_ENDPOINT,
                                          id_user)

            response = requests.get(url, timeout=cls.REQUESTS_TIMEOUT_SECONDS)
            json_payload = response.json()
            report = None

            if response.status_code == 200:
                report = json_payload

        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            return abort(500)

        return report
