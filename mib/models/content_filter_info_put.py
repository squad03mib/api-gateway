# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from mib.models.base_model_ import Model
from mib import util


class ContentFilterInfoPUT(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, filter_active: bool = None):  # noqa: E501
        """ContentFilterInfoPUT - a model defined in Swagger

        :param filter_active: The filter_active of this ContentFilterInfoPUT.  # noqa: E501
        :type filter_active: bool
        """
        self.swagger_types = {
            'filter_active': bool
        }

        self.attribute_map = {
            'filter_active': 'filter_active'
        }
        self._filter_active = filter_active

    @classmethod
    def from_dict(cls, dikt) -> 'ContentFilterInfoPUT':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The ContentFilterInfoPUT of this ContentFilterInfoPUT.  # noqa: E501
        :rtype: ContentFilterInfoPUT
        """
        return util.deserialize_model(dikt, cls)

    @property
    def filter_active(self) -> bool:
        """Gets the filter_active of this ContentFilterInfoPUT.

        status of the content filter  # noqa: E501

        :return: The filter_active of this ContentFilterInfoPUT.
        :rtype: bool
        """
        return self._filter_active

    @filter_active.setter
    def filter_active(self, filter_active: bool):
        """Sets the filter_active of this ContentFilterInfoPUT.

        status of the content filter  # noqa: E501

        :param filter_active: The filter_active of this ContentFilterInfoPUT.
        :type filter_active: bool
        """
        if filter_active is None:
            raise ValueError("Invalid value for `filter_active`, must not be `None`")  # noqa: E501

        self._filter_active = filter_active