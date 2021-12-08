# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from mib.models.base_model_ import Model
from mib import util


class Draft(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, id_draft: int=None, id_sender: int=None, recipients_list: List[object]=None, text: str=None, date_delivery: str=None, attachment_list: List[object]=None):  # noqa: E501
        """Draft - a model defined in Swagger

        :param id_draft: The id_draft of this Draft.  # noqa: E501
        :type id_draft: int
        :param id_sender: The id_sender of this Draft.  # noqa: E501
        :type id_sender: int
        :param recipients_list: The recipients_list of this Draft.  # noqa: E501
        :type recipients_list: List[object]
        :param text: The text of this Draft.  # noqa: E501
        :type text: str
        :param date_delivery: The date_delivery of this Draft.  # noqa: E501
        :type date_delivery: str
        :param attachment_list: The attachment_list of this Draft.  # noqa: E501
        :type attachment_list: List[object]
        """
        self.swagger_types = {
            'id_draft': int,
            'id_sender': int,
            'recipients_list': List[object],
            'text': str,
            'date_delivery': str,
            'attachment_list': List[object]
        }

        self.attribute_map = {
            'id_draft': 'id_draft',
            'id_sender': 'id_sender',
            'recipients_list': 'recipients_list',
            'text': 'text',
            'date_delivery': 'date_delivery',
            'attachment_list': 'attachment_list'
        }
        self._id_draft = id_draft
        self._id_sender = id_sender
        self._recipients_list = recipients_list
        self._text = text
        self._date_delivery = date_delivery
        self._attachment_list = attachment_list

    @classmethod
    def from_dict(cls, dikt) -> 'Draft':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Draft of this Draft.  # noqa: E501
        :rtype: Draft
        """
        return util.deserialize_model(dikt, cls)

    @property
    def id_draft(self) -> int:
        """Gets the id_draft of this Draft.

        Draft ID  # noqa: E501

        :return: The id_draft of this Draft.
        :rtype: int
        """
        return self._id_draft

    @id_draft.setter
    def id_draft(self, id_draft: int):
        """Sets the id_draft of this Draft.

        Draft ID  # noqa: E501

        :param id_draft: The id_draft of this Draft.
        :type id_draft: int
        """
        if id_draft is None:
            raise ValueError("Invalid value for `id_draft`, must not be `None`")  # noqa: E501

        self._id_draft = id_draft

    @property
    def id_sender(self) -> int:
        """Gets the id_sender of this Draft.

        Sender ID  # noqa: E501

        :return: The id_sender of this Draft.
        :rtype: int
        """
        return self._id_sender

    @id_sender.setter
    def id_sender(self, id_sender: int):
        """Sets the id_sender of this Draft.

        Sender ID  # noqa: E501

        :param id_sender: The id_sender of this Draft.
        :type id_sender: int
        """
        if id_sender is None:
            raise ValueError("Invalid value for `id_sender`, must not be `None`")  # noqa: E501

        self._id_sender = id_sender

    @property
    def recipients_list(self) -> List[object]:
        """Gets the recipients_list of this Draft.

        List of recipients IDs  # noqa: E501

        :return: The recipients_list of this Draft.
        :rtype: List[object]
        """
        return self._recipients_list

    @recipients_list.setter
    def recipients_list(self, recipients_list: List[object]):
        """Sets the recipients_list of this Draft.

        List of recipients IDs  # noqa: E501

        :param recipients_list: The recipients_list of this Draft.
        :type recipients_list: List[object]
        """

        self._recipients_list = recipients_list

    @property
    def text(self) -> str:
        """Gets the text of this Draft.

        Message text  # noqa: E501

        :return: The text of this Draft.
        :rtype: str
        """
        return self._text

    @text.setter
    def text(self, text: str):
        """Sets the text of this Draft.

        Message text  # noqa: E501

        :param text: The text of this Draft.
        :type text: str
        """
        if text is None:
            raise ValueError("Invalid value for `text`, must not be `None`")  # noqa: E501

        self._text = text

    @property
    def date_delivery(self) -> str:
        """Gets the date_delivery of this Draft.

        date of delivery  # noqa: E501

        :return: The date_delivery of this Draft.
        :rtype: str
        """
        return self._date_delivery

    @date_delivery.setter
    def date_delivery(self, date_delivery: str):
        """Sets the date_delivery of this Draft.

        date of delivery  # noqa: E501

        :param date_delivery: The date_delivery of this Draft.
        :type date_delivery: str
        """

        self._date_delivery = date_delivery

    @property
    def attachment_list(self) -> List[object]:
        """Gets the attachment_list of this Draft.

        list of attachment files base64 encoded  # noqa: E501

        :return: The attachment_list of this Draft.
        :rtype: List[object]
        """
        return self._attachment_list

    @attachment_list.setter
    def attachment_list(self, attachment_list: List[object]):
        """Sets the attachment_list of this Draft.

        list of attachment files base64 encoded  # noqa: E501

        :param attachment_list: The attachment_list of this Draft.
        :type attachment_list: List[object]
        """

        self._attachment_list = attachment_list