from mib.auth.user import User
from mib import app
from mib.models.content_filter import ContentFilter
from mib.models.content_filter_info_put import ContentFilterInfoPUT
from flask import abort
from flask_login import current_user
import requests
import json


class ContentFilterManager:
    CONTENT_FILTER_ENDPOINT = app.config['CONTENT_FILTER_MS_URL']
    REQUESTS_TIMEOUT_SECONDS = app.config['REQUESTS_TIMEOUT_SECONDS']

    @classmethod
    def get_content_filter_info(cls, content_filter_id: int) -> ContentFilter:
        ''' Get the content filter by id
        '''
        result = None
        try:
            url = "%s/users/%s/content_filter/%s" % (
                cls.CONTENT_FILTER_ENDPOINT, str(current_user.id), str(content_filter_id))
            response = requests.get(url, timeout=cls.REQUESTS_TIMEOUT_SECONDS)

            if response.status_code == 200:
                result = ContentFilter.from_dict(response.json())

            if response.status_code == 404:
                abort(404)

        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            return abort(500)
        return result

    '''@classmethod
    def get_content_filter_list(cls) -> ContentFilter:
        
        result = None
        try:
            url = "%s/users/%s/content_filter" % (
                cls.CONTENT_FILTER_ENDPOINT, str(current_user.id))
            response = requests.get(url, timeout=cls.REQUESTS_TIMEOUT_SECONDS)
            if response.status_code == 200:
                result = ContentFilter.from_dict(response.json())
            if response.status_code == 404:
                abort(404)

        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            return abort(500)

        return result '''

    @classmethod
    def set_content_filter(cls, content_filter_id: int, active: bool) -> ContentFilter:
        ''' Set the content filter by id
        '''
        result = None
        put_request = ContentFilterInfoPUT()
        put_request.filter_active = active
        try:
            url = "%s/users/%s/content_filter/%s" % (
                cls.CONTENT_FILTER_ENDPOINT, str(current_user.id), str(content_filter_id))
            response = requests.put(
                url, timeout=cls.REQUESTS_TIMEOUT_SECONDS, json=put_request.to_dict())
            if response.status_code == 200:
                result = ContentFilter.from_dict(response.json())

            if response.status_code == 404:
                abort(404)

            if response.status_code == 403:
                abort(403)

        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            return abort(500)

        return result
