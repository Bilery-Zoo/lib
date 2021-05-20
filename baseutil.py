#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
author    : Bilery Zoo(bilery.zoo@gmail.com)
create_ts : 2020-01-01
program   : *_* Microsoft Azure Blob service utility *_*
"""


def str_dict_key(_dict):
    """
    Convert dict keys in Python's built-in Bytes data type into formatted str type.
    """
    dict_ = {}
    for subs in _dict:
        dict_[subs.decode("utf-8")] = _dict[subs]
    return dict_


def str_dict_value(_dict):
    """
    Convert dict values in Python's built-in Bytes and / or other data types into formatted str type.
    """
    for subs in _dict:
        if _dict[subs]:
            try:
                _dict[subs] = _dict[subs].decode("utf-8")
            except AttributeError:
                _dict[subs] = str(_dict[subs])


def combine_lines_str(multi_line_str):
    """
    Convert str in lines into a single line.
    """
    single_line_str = ''
    for line in multi_line_str.split('\n'):
        if line:
            single_line_str += line.lstrip() + ' '
    return single_line_str
