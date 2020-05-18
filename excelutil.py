#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
author    : Bilery Zoo(bilery.zoo@gmail.com)
create_ts : 2020-04-06
program   : *_* excel file utility *_*
"""


import openpyxl


class Excel(object):
    def __init__(self, writer="data.xlsx", is_del_default=False, encoding="utf-8"):
        """
        Excel file init.
        :param writer: full path of Excel file to write out.
        :param is_del_default: whether or not to del default work sheet "Sheet" before saving workbook.
        :param encoding: encoding type.
        """
        self.writer = writer
        self.if_del_default = is_del_default
        self.encoding = encoding

        self.wkbook = openpyxl.Workbook()
        self.wkbook.encoding = self.encoding

    def __enter__(self):
        return self.wkbook

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.if_del_default:
            del self.wkbook["Sheet"]
        self.wkbook.save(self.writer)

    @staticmethod
    def get_sheet(wkbook, title=None, index=None):
        """
        Get an active sheet.
        :param title: work sheet title name.
        :param index: optional position at which the sheet will be inserted.
        """
        return wkbook.create_sheet(title, index) if title else wkbook.active

    @staticmethod
    def correct_int_row(row):
        """
        Correct int type of one line data(iterable) for Excel. See also
            https://support.office.com/en-us/article/display-numbers-in-scientific-exponential-notation-f85a96c0-18a1-4249-81c3-e934cd2aae25?ui=en-US&rs=en-US&ad=US
        :param row: a line of data(iterable) for Excel.
        """
        correct_row_list = []
        for _ in row:
            if isinstance(_, int) and len(str(_)) > 8:
                correct_row_list.append(str(_))
            else:
                correct_row_list.append(_)
        return correct_row_list


if __name__ == "__main__":
    header = ['name', 'rank', 'remark']
    record = [["Linux", 0, 12345678],
              ["MySQL", 1, 2238150616750203],
              ["MySQL", 1, "ありません"],
              ["Python", 2, "必須の箇所"],
              ["Python", 2, 123456789],
              ["Python", 2, 1234567890123]]
    with Excel("/home/zoo/jb.xlsx", True) as xlsx:
        wsheet = Excel.get_sheet(xlsx, title="data", index=0)
        wsheet.append(header)
        for _ in record:
            wsheet.append(Excel.correct_int_row(_))
