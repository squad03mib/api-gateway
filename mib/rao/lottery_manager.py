from mib.auth.user import User
from mib import app
from flask import abort
from flask_login import current_user
import requests
import json


class LotteryManager:
    LOTTERY_ENDPOINT = app.config['LOTTERY_MS_URL']
    REQUESTS_TIMEOUT_SECONDS = app.config['REQUESTS_TIMEOUT_SECONDS']

    @classmethod
    def get_lottery_by_id_user(cls, id_user: int):
        """
        This method contacts the lottery microservice
        and retrieves the lottery object by user id.
        :param id_user: the user id
        :return: Lottery obj with id_user=id_user
        """
        try:
            response = requests.get("%s/users/%s/lottery" % (cls.LOTTERY_ENDPOINT, str(id_user)),
                                    timeout=cls.REQUESTS_TIMEOUT_SECONDS)
            json_payload = response.json()

            if response.status_code == 200:
                lottery = json_payload
            else:
                raise RuntimeError(
                    'Server has sent an unrecognized status code %s' % response.status_code)

        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            return abort(500)

        return lottery

    @classmethod
    def create_lottery(cls, id_user: int, points: int, trials: int):
        try:
            url = "%s/users/%s/lottery" % (cls.LOTTERY_ENDPOINT,
                                           str(current_user.id))
            response = requests.post(url,
                                     json={
                                         'id_user': id_user,
                                         'points': points,
                                         'trials': trials
                                     },
                                     timeout=cls.REQUESTS_TIMEOUT_SECONDS
                                     )

        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            return abort(500)

        return response

    @classmethod
    def update_lottery(cls, id_user: int, points: int, trials: int):
        try:
            url = "%s/users/%s/lottery" % (cls.LOTTERY_ENDPOINT,
                                           str(current_user.id))
            response = requests.post(url,
                                     json={
                                         'id_user': id_user,
                                         'points': points,
                                         'trials': trials
                                     },
                                     timeout=cls.REQUESTS_TIMEOUT_SECONDS
                                     )

        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            return abort(500)

        return response
