#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
author    : Bilery Zoo(bilery.zoo@gmail.com)
create_ts : 2020-01-01
program   : *_* log logging handler *_*
"""


import sys
import logging
import functools


class LOG(object):
    """
    Log logging definition.
    """

    def __init__(self, level=logging.INFO, stream=sys.stdout, filename=None, filemode='a', datefmt="%Y-%m-%d %H:%M:%S",
                 format="%(asctime)s\t[%(levelname)s]\t< %(funcName)s[%(lineno)d] >\t%(message)s"):
        """
        LOG init.
        :param level: arg pass to standard library logging.basicConfig().
        :param stream: arg pass to standard library logging.basicConfig().
        :param filename: arg pass to standard library logging.basicConfig().
        :param filemode: arg pass to standard library logging.basicConfig().
        :param datefmt: arg pass to standard library logging.basicConfig().
        :param format: arg pass to standard library logging.basicConfig().
        """
        self.level = level
        self.stream = stream
        self.filename = filename
        self.filemode = filemode
        self.datefmt = datefmt
        self.format = format

    def formatted_logger(self, name=__name__):
        """
        Logger object generates.
        :param name: Logger name(parameters pass to standard library logging.getLogger()).
        :return: Logger object.
        """
        args = {
            "level": self.level,
            "stream": self.stream,
            "filename": self.filename,
            "filemode": self.filemode,
            "datefmt": self.datefmt,
            "format": self.format,
        }
        if not self.filename:
            del args["filename"]
        logging.basicConfig(**args)
        return logging.getLogger(name)

    def defined_logger(self, name=__name__):
        handler = logging.FileHandler(self.filename)
        handler.setFormatter(logging.Formatter(fmt=self.format, datefmt=self.datefmt))
        logger = logging.getLogger(name)
        logger.setLevel(self.level)
        logger.addHandler(handler)
        return logger

    @staticmethod
    def raise_log(raised_except, msg=''):
        """
        Raise exception by hand to escape error exit caused by built-in [raise].
        :param raised_except: Exception object.
        :param msg: Exception feedback message.
        :return: Python's built-in exit code.
            Output Exception of [raised_except].
        """
        try: raise raised_except(msg)
        except raised_except as E: logging.exception(E)

    @staticmethod
    def log(logger=None, exc_msg='', exit_msg='', check_msg='', check_except=None,
            is_begin_info=True, is_end_info=True, is_exit=False, is_result_check=False):
        """
        Log logging decorator function.
        :param logger: Logger object(see also logging.getLogger()).
        :param exc_msg: extra message to return when exceptions catch.
        :param if_exit: Boolean.
            Whether to exit or not when catching exception.
        :param exit_msg: extra message to return when exceptions catch and exit.
        :param is_result_check: Boolean.
            Whether or not to check Python's False status result of [func]'s return.
        :param check_except: Exception object to raise when [result_check].
        :param check_msg: Exception feedback message to return when [result_check].
        :return: decorated function [func]'s return.
        """
        if not logger: logger = LOG().formatted_logger()

        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                result = None
                try:
                    if is_begin_info: logger.info("Program enter into function\t< %s >" % func.__name__)
                    result = func(*args, **kwargs)
                except BaseException:
                    logger.exception(exc_msg)
                    if is_exit: sys.exit(exit_msg)
                else: return result
                finally:
                    if is_end_info: logger.info("Program leave function\t< %s >" % func.__name__)
                    if is_result_check and not result: LOG.raise_log(check_except, check_msg)
            return wrapper
        return decorator


if __name__ == "__main__":
    # Log = LOG()
    # Log.logger().info("INFO:info happened...")
    # Log.logger().error("ERROR:error happened...")
    # logging.basicConfig(filename="/var/PCR/err")
    # logging.error("ppp")
    # log = LOG(filename="/var/PCR/err").logger()
    # log.error("ppp")
    # l1 = LOG().formatted_logger()
    # l2 = LOG(filename="/var/PCR/jbd").formatted_logger()
    # l1.error("xxx")

    @LOG.log()
    def get(a, b):
        return a / b
    get(a=1, b=0)
