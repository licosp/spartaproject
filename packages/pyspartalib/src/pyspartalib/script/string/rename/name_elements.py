#!/usr/bin/env python

"""Module to take out name and index from base name of file."""

from re import sub

from pyspartalib.script.string.convert_type import convert_integer
from pyspartalib.script.string.rename.context.rename_context import BaseName
from pyspartalib.script.string.rename.split_identifier import SplitIdentifier


class NameElements(SplitIdentifier):
    """Class to take out name and index from base name of file."""

    def __initialize_super_class(self, identifier: str | None) -> None:
        super().__init__(identifier=identifier)

    def _get_name_elements(self, name: str, index: int) -> BaseName:
        return {
            "name": name,
            "index": index,
        }

    def _has_index(self, base_name: str) -> int | None:
        return convert_integer(
            sub("[a-z]", "", base_name.split(self.get_identifier())[-1]),
        )

    def _get_name(self, base_name: str) -> str:
        identifier: str = self.get_identifier()
        return identifier.join(base_name.split(identifier)[:-1])

    def split_name(self, base_name: str) -> BaseName | None:
        """Take out Name and Index Number from Base Name of File Name.

        Define of words.

        File Name: "group_type_v0001a.txt"
        Base Name: "group_type_v0001a"
        Split Identifier: "_"
        Name: "group_type"
        Index String: "v0001a"
        Index Number: 1

        e.g., return following data structure
            if you set Base Name above to argument "base_name".

        {
            name: "group_type"
            index: 1
        }

        Args:
            base_name (str): Base Name you want to get elements.

        Returns:
            BaseName | None: Elements generated by Base Name.
                It include Name as string and Index Number as integer.
                Return None if Base Name doesn't include Index String.

        """
        index: int | None = self._has_index(base_name)

        if index is None:  # Can't use Walrus Operator.
            return None

        return self._get_name_elements(self._get_name(base_name), index)

    def join_name(self, base_name: BaseName, digit: int = 4) -> str:
        """Convert elements including Name and Index Number to Base Name.

        Define of words.

        File Name: "group_type_0001.txt"
        Base Name: "group_type_0001"
        Split Identifier: "_"
        Name: "group_type"
        Index String: "0001"
        Index Number: 1

        Args:
            base_name (BaseName):
                Elements to construct Base Name of File Name,
                It include Name as string and Index Number as integer.

            digit (int, optional): Defaults to 4.
                Digit of Index String of Base Name.

        Returns:
            str: Base Name constructed from Name and Index Number.

        """
        return self.get_identifier().join(
            [base_name["name"], str(base_name["index"]).zfill(digit)],
        )

    def __init__(self, identifier: str | None = None) -> None:
        """Initialize variable of class.

        Args:
            identifier (str | None, optional): Defaults to None.
                Split identifier you selected.

        """
        self.__initialize_super_class(identifier)
