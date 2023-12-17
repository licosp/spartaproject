#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Module to edit internal of zip archive file."""

from pathlib import Path

from pyspartaproj.context.default.string_context import StrPair
from pyspartaproj.context.extension.path_context import Paths
from pyspartaproj.script.bool.compare_json import is_same_json
from pyspartaproj.script.directory.create_directory_temporary import WorkSpace
from pyspartaproj.script.file.archive.compress_zip import CompressZip
from pyspartaproj.script.file.archive.decompress_zip import DecompressZip
from pyspartaproj.script.file.json.convert_to_json import multiple_to_json
from pyspartaproj.script.path.iterate_directory import walk_iterator
from pyspartaproj.script.path.safe.safe_trash import SafeTrash
from pyspartaproj.script.time.stamp.get_timestamp import get_directory_latest


class EditZip(WorkSpace):
    """Class to edit internal of zip archive file.

    WorkSpace: Class to create temporary working directory shared in class.
    """

    def _initialize_variables(
        self, archive_path: Path, limit_byte: int
    ) -> None:
        self._still_removed: bool = False
        self._archive_path: Path = archive_path
        self._limit_byte: int = limit_byte

    def _get_archive_stamp(self) -> StrPair:
        return get_directory_latest(walk_iterator(self.get_root()))

    def _is_difference_archive(self) -> StrPair | None:
        archive_stamp: StrPair = self._get_archive_stamp()

        if is_same_json(
            *[
                multiple_to_json(stamp)
                for stamp in [self._archive_stamp, archive_stamp]
            ]
        ):
            return None

        return archive_stamp

    def _cleanup_before_override(self) -> None:
        safe_trash = SafeTrash()

        for path in self._decompressed:
            safe_trash.trash(path)

    def _compress_archive(self, archive_stamp: StrPair) -> Paths:
        self._cleanup_before_override()

        compress_zip = CompressZip(
            self._archive_path.parent, limit_byte=self._limit_byte
        )

        for path_text in archive_stamp.keys():
            compress_zip.compress_archive(
                Path(path_text), archive_root=self.get_root()
            )

        return compress_zip.close_archived()

    def _decompress_archive(self) -> None:
        decompress_zip = DecompressZip(self.get_root())
        self._decompressed: Paths = decompress_zip.sequential_archives(
            self._archive_path
        )

        for path in self._decompressed:
            decompress_zip.decompress_archive(path)

    def _initialize_archive(self) -> None:
        self._decompress_archive()
        self._archive_stamp: StrPair = self._get_archive_stamp()

    def _finalize_archive(self) -> Paths | None:
        archived: Paths | None = None

        if archive_stamp := self._is_difference_archive():
            archived = self._compress_archive(archive_stamp)

        super().__del__()

        return archived

    def get_decompressed_root(self) -> Path:
        return self.get_root()

    def close_archive(self) -> Paths | None:
        if self._still_removed:
            return None

        self._still_removed = True

        return self._finalize_archive()

    def __del__(self) -> None:
        self.close_archive()

    def __init__(self, archive_path: Path, limit_byte: int = 0) -> None:
        super().__init__()

        self._initialize_variables(archive_path, limit_byte)
        self._initialize_archive()
