

import hashlib
import os
import re
import sys
import traceback

from ipaddress import IPv4Address, IPv6Address, AddressValueError

from PyQt5 import QtCore
from PyQt5.QtCore import QCryptographicHash

from app.core.common.logapi import log


def trace_error_handler(logger):
    """
    Log the calling path of an exception

    :param logger: logger to use so traceback is logged to correct class
    :return:
    """
    log_string = "AppFTD Error trace"
    for tb in traceback.extract_stack():
        log_string = '{}\n   File {} at line {} \n\t called {}'.format(log_string, tb[0], tb[1], tb[3])
    logger.error(log_string)


def check_directory_exists(directory, do_not_log=False):
    """
    Check a directory exists and if not create it

    :param directory: The directory to make sure exists
    :param do_not_log: To not log anything. This is need for the start up, when the log isn't ready
    :return:
    """
    if not do_not_log:
        log.debug('check_directory_exists {}'.format(directory))
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except IOError:
        if not do_not_log:
            log.exception('failed to check if directory exists or create directory')


def translate(context, text, comment=None, qt_translate=QtCore.QCoreApplication.translate):
    """
    A special shortcut method to wrap around the Qt5 translation functions.
    This abstracts the translation procedure so that we can change it if at a
    later date if necessary, without having to redo the whole of AppFTD.

    :param context: The translation context, used to give each string a context or a namespace
    :param text: The text to put into the translation tables for translation
    :param comment: An identifying string for when the same text is used in different roles within the same context
    :param qt_translate:
    :return:
    """
    return qt_translate(context, text, comment)


def de_hump(name):
    """
    Change any Camel Case string to python string

    :param name:
    :return:
    """
    first_camel_case = re.compile('(.)([A-Z][a-z]+)')
    second_camel_case = re.compile('([a-z0-9])([A-Z])')

    sub_name = first_camel_case.sub(r'\1_\2', name)
    return second_camel_case.sub(r'\1_\2', sub_name).lower()


def is_win():
    """
    Returns true if running on a system with a nt kernel e.g. Windows, Wine

    :return: True if system is running a nt kernel false otherwise
    """
    return os.name.startswith('nt')


def is_macosx():
    """
    Returns true if running on a system with a darwin kernel e.g. Mac OS X

    :return: True if system is running a darwin kernel false otherwise
    """
    return sys.platform.startswith('darwin')


def is_linux():
    """
    Returns true if running on a system with a linux kernel e.g. Ubuntu, Debian, etc

    :return: True if system is running a linux kernel false otherwise
    """
    return sys.platform.startswith('linux')
