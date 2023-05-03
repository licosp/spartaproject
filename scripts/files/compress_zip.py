#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from zipfile import ZipFile, ZipInfo, ZIP_LZMA, ZIP_STORED

from contexts.decimal_context import Decimal, set_decimal_context
from contexts.integer_context import IntTuple
from contexts.string_context import Strs
from contexts.path_context import Path, Paths
from scripts.files.import_file import byte_import
from scripts.files.export_json import json_dump, Json
from scripts.paths.get_relative import path_relative
from scripts.paths.create_directory import path_mkdir
from scripts.paths.iterate_directory import walk_iterator
from scripts.times.get_timestamp import get_latest, get_access

set_decimal_context()


def _default() -> int:
    limit_byte: int = 1
    for _ in range(3):
        limit_byte *= (2**10)
    return limit_byte * 4


class CompressZip:
    def __init__(
            self, output_root: Path,
            archive_id: str = '',
            limit_byte: int = _default(),
            compress: bool = False,
    ) -> None:
        self._output_root: Path = output_root

        self._limit_byte: Decimal = Decimal(str(limit_byte))
        self._compress: bool = compress

        self._init_archive_id(archive_id)
        self._init_walk_history()
        self._init_archive_output()

    def _init_archive_id(self, archive_id: str) -> None:
        if 0 == len(archive_id):
            archive_id = self._output_root.name
        self._archive_id = archive_id

    def _init_walk_history(self) -> None:
        self._walk_directories: Paths = []
        self._walk_files: Paths = []
        self._archived: Paths = []

    def _init_archive_output(self) -> None:
        self._output_index: int = 0
        path_mkdir(self._output_root)

    def close_archived(self) -> Paths:
        self._file_zip.close()
        return self._archived

    def _has_archived(self) -> bool:
        return 0 < self._output_index

    def _get_archive_path(self) -> Path:
        file_names: Strs = [self._archive_id]

        if self._has_archived():
            file_names += [str(self._output_index).zfill(4)]
        self._output_index += 1

        return Path(self._output_root, '_'.join(file_names)).with_suffix('.zip')

    def _reset_archive_byte(self) -> None:
        self._archived += [self._get_archive_path()]
        self._file_zip = ZipFile(
            self._archived[-1],
            mode='w',
        )

    def _convert_comment(self, attribute: Json) -> bytes:
        comment: str = json_dump(attribute)
        return comment.encode('utf-8')

    def _get_time_comment(self, target: Path) -> bytes:
        return self._convert_comment({'time': {
            type: func(target).isoformat()
            for type, func in zip(['latest', 'access'], [get_latest, get_access])
        }})

    def _get_time_latest(self, target: Path) -> IntTuple:
        time: datetime = get_latest(target)
        return (time.year, time.month, time.day, time.hour, time.minute, time.second)

    def _get_zip_info(self, target: Path, relative: Path) -> ZipInfo:
        zip_info: ZipInfo = ZipInfo(filename=str(relative))

        zip_info.compress_type = (ZIP_LZMA if self._compress else ZIP_STORED)
        zip_info.comment = self._get_time_comment(target)
        zip_info.date_time = self._get_time_latest(target)

        return zip_info

    def _add_file_to_archive(self, is_dir: bool, reset: bool, target: Path, root: Path) -> None:
        if reset:
            self._reset_archive_byte()

        relative: Path = path_relative(target, root_path=root)
        if is_dir:
            self._file_zip.mkdir(str(relative))
        else:
            self._file_zip.writestr(
                self._get_zip_info(target, relative),
                byte_import(target),
            )

    def _within_allowance(self, target_byte: Decimal) -> bool:
        return self._limit_byte >= target_byte

    def _archive_outside_byte(self) -> Decimal:
        current_archive: Path = self._archived[-1]
        return Decimal(str(current_archive.stat().st_size))

    def _archive_inside_byte(self) -> Decimal:
        return Decimal(str(sum([info.file_size for info in self._file_zip.infolist()])))

    def _archive_include_files(self) -> bool:
        return 0 < self._archive_inside_byte()

    def _estimate_compressed_size(self, src_byte: Decimal) -> Decimal:
        outside_byte: Decimal = self._archive_outside_byte()
        inside_byte: Decimal = self._archive_inside_byte()

        return src_byte * (outside_byte / inside_byte)

    def _estimate_archived_size(self, src_byte: Decimal) -> Decimal:
        outside_byte: Decimal = self._archive_outside_byte()
        return src_byte + outside_byte

    def _update_archive_byte(self, target: Path, root: Path) -> None:
        archive_reset: bool = False

        if self._has_archived():
            src_byte: Decimal = Decimal(str(target.stat().st_size))
            include_files: bool = self._archive_include_files()

            if include_files:
                src_byte = self._estimate_compressed_size(src_byte)

            if self._within_allowance(src_byte):
                if include_files:
                    if not self._within_allowance(self._estimate_archived_size(src_byte)):
                        archive_reset = True
            elif include_files:
                archive_reset = True
        else:
            archive_reset = True

        self._add_file_to_archive(False, archive_reset, target, root)

    def _not_still_archived(self, is_dir: bool, target: Path) -> bool:
        archived: Paths = self._walk_directories if is_dir else self._walk_files

        not_still: bool = target not in archived
        if not_still:
            archived += [target]

        return not_still

    def _add_archive_child(self, target: Path, root: Path) -> None:
        if target.is_dir():
            if self._not_still_archived(True, target):
                archive_reset: bool = not self._has_archived()
                self._add_file_to_archive(True, archive_reset, target, root)

                for path in walk_iterator(target):
                    self._add_archive_child(path, root)
        else:
            if self._not_still_archived(False, target):
                self._update_archive_byte(target, root)

    def add_archive(self, archive_target: Path, archive_root: Path = Path('')) -> None:
        if archive_target.is_relative_to(archive_root):
            self._add_archive_child(archive_target, archive_root)
        else:
            self._add_archive_child(archive_target, archive_target.parent)
