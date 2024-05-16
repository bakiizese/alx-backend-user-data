#!/usr/bin/env python3
''' filter '''
import re


def filter_datum(fields, redaction, message, separetor):
    ''' filter '''
    for i in fields:
        pattern = r"({}=)([^;]+)".format(i)
        mess = re.sub(pattern, r"\1{}".format(redaction), message)
        message = mess
    return mess
