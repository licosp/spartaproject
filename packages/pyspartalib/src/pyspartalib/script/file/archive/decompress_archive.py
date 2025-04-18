#!/usr/bin/env python

"""Module to decompress file or directory by archive format."""

from datetime import UTC, datetime
from os import sep
from pathlib import Path
from zipfile import ZIP_LZMA, ZipFile, ZipInfo

from pyspartalib.context.default.string_context import StrPair, Strs
from pyspartalib.context.extension.path_context import Paths
from pyspartalib.script.directory.create_directory import create_directory
from pyspartalib.script.directory.create_parent import create_parent
from pyspartalib.script.file.archive.archive_format import get_format
from pyspartalib.script.file.json.convert_from_json import (
    string_pair_from_json,
)
from pyspartalib.script.file.json.import_json import json_load
from pyspartalib.script.file.text.export_file import byte_export
from pyspartalib.script.path.iterate_directory import walk_iterator
from pyspartalib.script.string.convert_type import convert_integer
from pyspartalib.script.string.encoding.set_decoding import set_decoding
from pyspartalib.script.time.path.set_timestamp import set_latest


class DecompressArchive:
    """Class to decompress file or directory by archive format."""

    def _initialize_paths(self, output_root: Path) -> None:
        self._output_root: Path = output_root

    def _is_sequential_archive(self, path: Path) -> bool:
        names: Strs = path.stem.split("#")

        if len(names) > 1:
            index: int | None = convert_integer(names[-1])

            if index is not None:  # Can't use Walrus Operator.
                return True

        return False

    def _decompress_file(
        self,
        file_path: Path,
        information: ZipInfo,
        archive_file: ZipFile,
    ) -> None:
        create_parent(file_path)
        byte_export(file_path, archive_file.read(information.filename))

    def _get_content(self, comment: bytes) -> StrPair:
        return string_pair_from_json(json_load(set_decoding(comment)))

    def _restore_timestamp(
        self,
        file_path: Path,
        information: ZipInfo,
    ) -> None:
        latest: datetime = datetime(*information.date_time, tzinfo=UTC)
        comment: bytes = information.comment

        if len(comment) > 0:
            content: StrPair = self._get_content(comment)

            if "latest" in content:
                latest = datetime.fromisoformat(content["latest"])

        set_latest(file_path, latest)

    def _encode_multiple(self, text: str) -> bytes:
        return text.encode("cp437", errors="ignore")

    def _decode_multiple(self, byte: bytes) -> str:
        return byte.decode("cp932")

    def _get_separator(self) -> str:
        return "/"

    def _convert_multiple(self, text: str) -> str | None:
        byte: bytes = self._encode_multiple(text)

        if len(text) != len(byte):
            return None

        return self._decode_multiple(byte)

    def _support_multiple_byte(self, text: str) -> str:
        if converted := self._convert_multiple(text):
            separator: str = self._get_separator()

            if separator == sep:
                return converted

            if sep not in converted:
                return converted

            return converted.replace(sep, separator)

        return text

    def _get_file_path(self, information: ZipInfo) -> Path:
        return Path(
            self._output_root,
            Path(self._support_multiple_byte(information.orig_filename)),
        )

    def sequential_archives(self, source_archive: Path) -> Paths:
        """Get list of archives which is compressed dividedly.

        Args:
            source_archive (Path): The head path of sequential archives.

        Returns:
            Paths: List of paths of sequential archives you got.

        e.g., sequential archives dividedly to three are represented to follow.

            root/
                |--archive.<archive format>
                |--archive#0001.<archive format>
                |--archive#0002.<archive format>

        If you select path "source_archive" is "root/archive.<archive format>",
            following list is returned.

            [
                root/archive.<archive format>,
                root/archive#0001.<archive format>,
                root/archive#0002.<archive format>
            ]

        Name format of sequential archives are follow.

        Index 0:    <archive name>.<archive format>
        Index 1~:   <archive name>#<string index>.<archive format>

        <archive name> of all indices must be same.
        <string index> must filled by zero, and digit is optional.

        """
        return [
            source_archive,
            *[
                path
                for path in walk_iterator(
                    source_archive.parent,
                    directory=False,
                    depth=1,
                    suffix=get_format(),
                )
                if (source_archive != path)
                and self._is_sequential_archive(path)
            ],
        ]

    def decompress_archive(self, decompress_target: Path) -> None:
        """Decompress file or directory by archive format.

        Args:
            decompress_target (Path): Path of archive you want to decompress.

        """
        with ZipFile(decompress_target) as archive_file:
            for information in archive_file.infolist():
                file_path: Path = self._get_file_path(information)

                if information.is_dir():
                    create_directory(file_path)
                else:
                    self._decompress_file(file_path, information, archive_file)
                    self._restore_timestamp(file_path, information)

    def decompress_at_once(self, paths: Paths) -> None:
        """Decompress list of file or directory at once.

        Args:
            paths (Paths): List of path you want to decompress.

        """
        for path in paths:
            self.decompress_archive(path)

    def is_lzma_archive(self, decompress_target: Path) -> bool:
        """Get status of compression format.

        Args:
            decompress_target (Path): Path of archive
                which you want to get status of compression format.

        Returns:
            bool: True if archive is compressed by LZMA.

        """
        with ZipFile(decompress_target) as archive_file:
            for information in archive_file.infolist():
                if information.compress_type == ZIP_LZMA:
                    return True

        return False

    def __init__(self, output_root: Path) -> None:
        """Initialize decompress directory.

        Args:
            output_root (Path): Path of decompress directory.

        """
        self._initialize_paths(output_root)
