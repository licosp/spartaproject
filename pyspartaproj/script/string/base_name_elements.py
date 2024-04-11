#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Module to take out name and index from base name of file."""

from re import sub

from pyspartaproj.context.default.string_context import Strs
from pyspartaproj.context.typed.user_context import BaseName
from pyspartaproj.script.string.convert_type import convert_integer


class BaseNameElements:
    """Class to take out name and index from base name of file."""

    def _initialize_variables(self) -> None:
        self._split_identifier = "_"

    def _get_name_elements(self, name: str, index: int) -> BaseName:
        return {
            "name": name,
            "index": index,
        }

    def _has_index(self, base_name: str) -> int | None:
        return convert_integer(
            sub("[a-z]", "", base_name.split(self._split_identifier)[-1])
        )

    def _get_name(self, base_name: str) -> str:
        identifier: str = self._split_identifier
        return identifier.join(base_name.split(identifier)[:-1])

    def split_name(self, base_name: str) -> BaseName | None:
        """Take out name and index from base name of file.

        Define of words.

        File Name: "group_type_v0001a.txt"
        Base Name: "group_type_v0001a"
        Split Identifier: "_"
        Name: "group_type"
        Index: "v0001a"
        Index Number: 1

        e.g., return following data structure
            if you set string "File Name" above to argument "base_name".

        {
            name: "group_type"
            index: 1
        }

        Args:
            name (str): Name of file you want to get elements.

        Returns:
            BaseName | None: Elements generated by name of file.
                Return None if base name does not include index string.
        """
        if index := self._has_index(base_name):
            return self._get_name_elements(self._get_name(base_name), index)

        return None

    def __init__(self) -> None:
        """Initialize variable of class."""
        self._initialize_variables()
