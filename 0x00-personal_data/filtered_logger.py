#!/usr/bin/env python3
''' filter '''
import re


def filter_datum(fields, redaction, message, separetor) -> str:
    ''' filter '''
    for i in fields:
        pattern = r"({}=)([^;]+)".format(i)
        message = re.sub(pattern, r"\1{}".format(redaction), message)
    return message
