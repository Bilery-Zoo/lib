#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
author    : Bilery Zoo(bilery.zoo@gmail.com)
create_ts : 2020-04-18
program   : *_* mail service utility *_*
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class Smtp(object):
    def __init__(self, host, user, password, port=25):
        """
        SMTP server init. See also
            https://docs.python.org/2.7/library/smtplib.html
        :param host: SMTP server host.
        :param user: SMTP server user.
        :param password: SMTP server password.
        :param port: SMTP server port.
        """
        self.host = host
        self.port = port
        self.user = user
        self.password = password

        self.smtp = smtplib.SMTP()

    def __enter__(self):
        self.smtp.connect(host=self.host, port=self.port)
        self.smtp.login(user=self.user, password=self.password)
        return self.smtp

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.smtp.quit()


class Mail(object):
    def __init__(self, _from, _to, _cc=None, _bcc=None, _subject='', _body='', _attach=None):
        """
        Mail object init. See also
            https://docs.python.org/2.7/
            https://tools.ietf.org/html/rfc4021
        There is a BUG remained that `cc` and `bcc` accounts display in recipients list and can not be hidden. See also
            https://stackoverflow.com/questions/1546367/python-how-to-send-mail-with-to-cc-and-bcc
        :param _from: mail sender.
        :param _to: mail recipients list.
        :param _cc: mail cc recipients list.
        :param _bcc: mail bcc recipients list.
        :param _subject: mail subject.
        :param _body: mail body.
        :param _attach: mail attachments list.
        """
        self._from = _from
        self._to = _to
        self._cc = _cc
        self._bcc = _bcc
        self._subject = _subject
        self._body = _body
        self._attach = _attach

    def construct_mail(self):
        msg = MIMEMultipart()
        msg['From'] = self._from
        msg['To'] = ','.join(self._to)
        if self._cc:
            msg["Cc"] = ','.join(self._cc)
        if self._bcc:
            msg["Bcc"] = ','.join(self._bcc)
        msg['subject'] = self._subject
        msg.attach(MIMEText(self._body, _charset="utf-8"))
        if self._attach:
            for _ in self._attach:
                msg_attach = MIMEText(open(_[0] + _[1], "rb").read(), _subtype="base64", _charset="utf-8")
                msg_attach.add_header("Content-Disposition", "attachment", filename=_[1])
                msg_attach["Content-Type"] = "application/octet-stream"
                msg.attach(msg_attach)
        return msg

    def send_mail(self, smtp):
        tos = self._to
        if self._cc:
            tos += self._cc
        if self._bcc:
            tos += self._bcc
        smtp.sendmail(self._from, tos, self.construct_mail().as_string())


if __name__ == "__main__":
    SMTP = {
        "host": "smtp.net",
        "port": 587,
        "user": "key",
        "password": "BrA",
    }
    MAIL = {
        "_from": "noreply@co.jp",
        "_to": ["@co.jp"],
        "_cc": ["@gmail.com", "@qq.com"],
        "_subject": "test mail",
        "_body": "test mail\n\t(generate by Python2.7.17)",
        "_attach": [["/", "dd.xlsx", ], ],
    }
    with Smtp(**SMTP) as s:
        Mail(**MAIL).send_mail(s)
