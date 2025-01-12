#!/usr/bin/env python

"""Test module to convert data to json format."""

from decimal import Decimal
from pathlib import Path

from pyspartalib.context.default.bool_context import (
    BoolPair,
    BoolPair2,
    Bools,
    Bools2,
)
from pyspartalib.context.default.float_context import (
    FloatPair,
    FloatPair2,
    Floats,
    Floats2,
)
from pyspartalib.context.default.integer_context import (
    IntPair,
    IntPair2,
    Ints,
    Ints2,
)
from pyspartalib.context.default.string_context import (
    StrPair,
    StrPair2,
    Strs,
    Strs2,
)
from pyspartalib.context.extension.decimal_context import (
    DecPair,
    DecPair2,
    Decs,
    Decs2,
)
from pyspartalib.context.extension.path_context import (
    PathPair,
    PathPair2,
    Paths,
    Paths2,
)
from pyspartalib.context.file.json_context import Json, Multi, Multi2
from pyspartalib.script.file.json.convert_to_json import (
    multiple2_to_json,
    multiple_to_json,
    to_safe_json,
)
from pyspartalib.script.file.json.export_json import json_dump


def _common_test(expected: str, source: Json) -> None:
    assert expected == json_dump(source, compress=True)


def _common_test_array(expected: str, source_array: Multi) -> None:
    expected_array: str = f"[{expected}]"
    _common_test(expected_array, multiple_to_json(source_array))


def _common_test_array2(expected: str, source_arrays: Multi2) -> None:
    expected_array: str = f"[[{expected}]]"
    _common_test(expected_array, multiple2_to_json(source_arrays))


def _common_test_pair(expected: str, source_pair: Multi) -> None:
    expected_pair: str = '{"B":%s}' % expected
    _common_test(expected_pair, multiple_to_json(source_pair))


def _common_test_pair2(expected: str, source_pairs: Multi2) -> None:
    expected_pair: str = """{"A":{"B":%s}}""" % expected
    _common_test(expected_pair, multiple2_to_json(source_pairs))


def test_bool_array() -> None:
    """Test to convert data which is list of type "bool"."""
    source: bool = True
    source_array: Bools = [source]
    source_arrays: Bools2 = [source_array]
    expected: str = "true"

    _common_test_array(expected, source_array)
    _common_test_array2(expected, source_arrays)


def test_bool_pair() -> None:
    """Test to convert data which is dictionary of type "bool"."""
    source: bool = True
    source_pair: BoolPair = {"B": source}
    source_pairs: BoolPair2 = {"A": source_pair}
    expected: str = "true"

    _common_test_pair(expected, source_pair)
    _common_test_pair2(expected, source_pairs)


def test_integer_array() -> None:
    """Test to convert data which is list of type "int"."""
    source: int = 1
    source_array: Ints = [source]
    source_arrays: Ints2 = [source_array]
    expected: str = "1"

    _common_test_array(expected, source_array)
    _common_test_array2(expected, source_arrays)


def test_integer_pair() -> None:
    """Test to convert data which is dictionary of type "int"."""
    source: int = 1
    source_pair: IntPair = {"B": source}
    source_pairs: IntPair2 = {"A": source_pair}
    expected: str = "1"

    _common_test_pair(expected, source_pair)
    _common_test_pair2(expected, source_pairs)


def test_float_array() -> None:
    """Test to convert data which is list of type "float"."""
    source: float = 1.0
    source_array: Floats = [source]
    source_arrays: Floats2 = [source_array]
    expected: str = "1.0"

    _common_test_array(expected, source_array)
    _common_test_array2(expected, source_arrays)


def test_float_pair() -> None:
    """Test to convert data which is dictionary of type "float"."""
    source: float = 1.0
    source_pair: FloatPair = {"B": source}
    source_pairs: FloatPair2 = {"A": source_pair}
    expected: str = "1.0"

    _common_test_pair(expected, source_pair)
    _common_test_pair2(expected, source_pairs)


def test_string_array() -> None:
    """Test to convert data which is list of type "str"."""
    source: str = "R"
    source_array: Strs = [source]
    source_arrays: Strs2 = [source_array]
    expected: str = '"R"'

    _common_test_array(expected, source_array)
    _common_test_array2(expected, source_arrays)


def test_string_pair() -> None:
    """Test to convert data which is dictionary of type "str"."""
    source: str = "R"
    source_pair: StrPair = {"B": source}
    source_pairs: StrPair2 = {"A": source_pair}
    expected: str = '"R"'

    _common_test_pair(expected, source_pair)
    _common_test_pair2(expected, source_pairs)


def test_decimal_array() -> None:
    """Test to convert data which is list of type "Decimal"."""
    source: Decimal = Decimal("1.0")
    source_array: Decs = [source]
    source_arrays: Decs2 = [source_array]
    expected: str = "1.0"

    _common_test_array(expected, source_array)
    _common_test_array2(expected, source_arrays)


def test_decimal_pair() -> None:
    """Test to convert data which is dictionary of type "Decimal"."""
    source: Decimal = Decimal("1.0")
    source_pair: DecPair = {"B": source}
    source_pairs: DecPair2 = {"A": source_pair}
    expected: str = "1.0"

    _common_test_pair(expected, source_pair)
    _common_test_pair2(expected, source_pairs)


def test_path_array() -> None:
    """Test to convert data which is list of type "Path"."""
    source: Path = Path("root")
    source_array: Paths = [source]
    source_arrays: Paths2 = [source_array]
    expected: str = '"root"'

    _common_test_array(expected, source_array)
    _common_test_array2(expected, source_arrays)


def test_path_pair() -> None:
    """Test to convert data which is dictionary of type "Path"."""
    source: Path = Path("root")
    source_pair: PathPair = {"B": source}
    source_pairs: PathPair2 = {"A": source_pair}
    expected: str = '"root"'

    _common_test_pair(expected, source_pair)
    _common_test_pair2(expected, source_pairs)


def test_tree() -> None:
    """Test to convert custom json format data to default json format."""
    source_pairs: Json = {
        "A": {"B": {"C": [None, Decimal("-1.0"), Path("root")]}}
    }
    expected: str = """{"A":{"B":{"C":[null,-1.0,"root"]}}}"""
    assert expected == json_dump(to_safe_json(source_pairs), compress=True)
