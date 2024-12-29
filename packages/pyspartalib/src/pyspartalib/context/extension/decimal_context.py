#!/usr/bin/env python

"""User defined types about type "Decimal"."""

from decimal import Decimal
from typing import Dict, List

DecPair = dict[str, Decimal]
Decs = list[Decimal]

DecPair2 = dict[str, DecPair]
Decs2 = list[Decs]
