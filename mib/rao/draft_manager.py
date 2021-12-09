from typing import List

from mib import app
from mib.models import Draft, DraftPost, Message
from flask import abort
import requests
from flask_login import current_user

class DraftManager:
    MESSAGES_ENDPOINT = app.config['MESSAGES_MS_URL']
    REQUESTS_TIMEOUT_SECONDS = app.config['REQUESTS_TIMEOUT_SECONDS']

    @classmethod
    def delete_draft(cls, draft_id :int) -> int:
        """
        Delete a draft by its id

        :param draft_id: Draft Unique ID
        :type draft_id: int

        :rtype: int
        """
        status = 0
        try:

            url = "%s/drafts/%s?current_user_id=%s" % (cls.MESSAGES_ENDPOINT, draft_id, current_user.id)
            response = requests.delete(url, timeout=cls.REQUESTS_TIMEOUT_SECONDS)
            status = response.status_code

        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            return abort(500)

        return status

    @classmethod
    def get_all_drafts(cls) -> List[Draft]:
        """
        Get all drafts list # noqa: E501


        :rtype: List[Draft]
        """
        draft_list = []
        try:
            
            url = "%s/drafts?current_user_id=%s" % (cls.MESSAGES_ENDPOINT, current_user.id)
            response = requests.get(url, timeout=cls.REQUESTS_TIMEOUT_SECONDS)
            if response.status_code == 200:
                for item in response.json():
                    draft_list.append(Draft().from_dict(item))

        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            return abort(500)

        return draft_list

    @classmethod
    def get_draft(cls, draft_id :int) -> Draft:
        """
        Get a draft by its id # noqa: E501

        :param draft_id: Draft Unique ID
        :type draft_id: int

        :rtype: Draft
        """
        draft = None
        try:
            
            url = "%s/drafts/%s?current_user_id=%s" % (cls.MESSAGES_ENDPOINT, draft_id, current_user.id)
            response = requests.get(url, timeout=cls.REQUESTS_TIMEOUT_SECONDS)
            if response.status_code == 200:
                draft = Draft().from_dict(response.json())

        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            return abort(500)

        return draft

    @classmethod
    def save_draft(cls, draft :DraftPost) -> Draft:
        """
        Create a new draft

        :param draft: A new draft
        :type draft: DraftPost

        :rtype: Draft
        """
        new_draft = None
        try:
            
            url = "%s/drafts?current_user_id=%s" % (cls.MESSAGES_ENDPOINT, current_user.id)
            response = requests.post(url,
                json=draft.to_dict(), timeout=cls.REQUESTS_TIMEOUT_SECONDS)
            if response.status_code == 201:
                new_draft = Draft().from_dict(response.json())

        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            return abort(500)

        return new_draft

    @classmethod
    def send_draft(cls, draft_id :int) -> Message:
        """
        Send a draft by its id

        :param draft_id: Draft Unique ID
        :type draft_id: int

        :rtype: Message
        """
        message = None
        try:
            
            url = "%s/drafts/%s/send?current_user_id=%s" % (cls.MESSAGES_ENDPOINT, draft_id, current_user.id)
            response = requests.post(url, timeout=cls.REQUESTS_TIMEOUT_SECONDS)
            if response.status_code == 200:
                message = Message().from_dict(response.json())

        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            return abort(500)

        return message