#!/usr/bin/env python3
''' filter '''
import re
from typing import List


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    ''' filter '''
    return re.sub(rf"({'|'.join(fields)})=[^;{separator}]+",
                  lambda m: f"{m.group(1)}={redaction}", message)
