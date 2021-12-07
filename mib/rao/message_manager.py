from typing import List

from mib import app
from mib.models import Message, MessagePost
from flask import abort
import requests
from flask_login import current_user

class MessageManager:
    MESSAGES_ENDPOINT = app.config['MESSAGES_MS_URL']
    REQUESTS_TIMEOUT_SECONDS = app.config['REQUESTS_TIMEOUT_SECONDS']

    @classmethod
    def delete_message(cls, message_id :int) -> int:
        """
        Delete a message by its id

        :param message_id: Message Unique ID
        :type message_id: int

        :rtype: int
        """
        status = 0
        try:

            url = "%s/messages/%s?current_user_id=%s" % (cls.MESSAGES_ENDPOINT, message_id, current_user.id)
            response = requests.delete(url, timeout=cls.REQUESTS_TIMEOUT_SECONDS)
            status = response.status_code

        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            return abort(500)

        return status

    @classmethod
    def get_all_messages(cls, type :str) -> List[Message]:
        """
        Get all messages list

        :param type: The types of messages to retrieve
        :type type: str

        :rtype: List[Message]
        """
        message_list = []
        try:
            
            url = "%s/messages?type=%s&current_user_id=%s" % (cls.MESSAGES_ENDPOINT, type, current_user.id)
            response = requests.get(url, timeout=cls.REQUESTS_TIMEOUT_SECONDS)
            if response.status_code == 200:
                for item in response.json():
                    message_list.append(Message().from_dict(item))

        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            return abort(500)

        return message_list

    @classmethod
    def get_message(cls, message_id :int) -> Message:
        """
        Get a message by its id

        :param message_id: Message Unique ID
        :type message_id: int

        :rtype: Message
        """
        message = None
        try:
            
            url = "%s/messages/%s?current_user_id=%s" % (cls.MESSAGES_ENDPOINT, message_id, current_user.id)
            response = requests.get(url, timeout=cls.REQUESTS_TIMEOUT_SECONDS)
            if response.status_code == 200:
                message = Message().from_dict(response.json())

        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            return abort(500)

        return message

    @classmethod
    def send_message(cls, msg :MessagePost) -> Message:
        """
        Send a new message

        :param message: message to send
        :type body: MessagePost

        :rtype: Message
        """
        message = None
        try:
            
            url = "%s/messages?current_user_id=%s" % (cls.MESSAGES_ENDPOINT, current_user.id)
            response = requests.post(url,
                json=msg.to_dict(), timeout=cls.REQUESTS_TIMEOUT_SECONDS)
            if response.status_code == 201:
                message = Message().from_dict(response.json())

        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            return abort(500)

        return message

    @classmethod
    def withdraw_message(cls, message_id :int) -> int:
        """
        Withdraw a sent message by its id

        :param message_id: Message Unique ID
        :type message_id: int

        :rtype: int
        """
        status = 0
        try:
            
            url = "%s/messages/%s/withdraw?current_user_id=%s" % (cls.MESSAGES_ENDPOINT, message_id, current_user.id)
            response = requests.post(url, timeout=cls.REQUESTS_TIMEOUT_SECONDS)
            status = response.status_code

        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            return abort(500)

        return status

