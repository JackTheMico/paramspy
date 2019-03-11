# -*- coding:utf-8 -*-
"""
-------------------------------------------------

    File Name:        /Users/jackdeng/code/Python/paramspy/tests/test_check.py

    Description:      test for checker

    Author:           dlwxxxdlw@163.com

    Date:             2019-03-10-14:11:45

    Version:          v1.0

    Lastmodified:     2019-03-10 by Jack Deng

-------------------------------------------------
"""

import re
import pytest
try:
    from loguru import logger
except ImportError:
    from logging import getLogger
    logger = getLogger(__name__)

from paramspy import Checker, CheckFailed, RuleNotMatch


def test_one_rule_not_match():
    target = {
        "username": "dlwxxxdlw",
        "password": "zxvxcgweg",
        "phone": "1234567890%$^",
    }

    try:
        res = Checker([
            ["username", None, "WORD"],
            ["password", None, "WORD"],
            ["phone", None, "NUMBER"],
            ["gender", "female"]
        ]).check(target)
    except CheckFailed as check_err:
        assert isinstance(check_err.args[0][0], RuleNotMatch)
        logger.error("one_rule_not_match err {}".format(check_err))

def test_multi_rule_not_match():
    target = {
        "username": "dlwxxxdlw",
        "password": "zxvxcgweg",
        "phone": "1234567890%$^",
        "email": "heheeheheda"
    }

    try:
        res = Checker([
            ["username", None, "WORD"],
            ["password", None, "WORD"],
            ["phone", None, "NUMBER"],
            ["gender", "female"],
            ["email", None, "EMAIL"]
        ]).check(target)
    except CheckFailed as check_err:
        assert isinstance(check_err.args[0][0], RuleNotMatch)
        assert isinstance(check_err.args[0][1], RuleNotMatch)
        logger.error("multi_rule_not_match err {}".format(check_err))

def test_all_match():
    target = {
        "username": "dlwxxxdlw",
        "password": "zxvxcgweg",
        "phone": "1234567890",
        "email": "heheeheheda@gmail.com"
    }

    try:
        res = Checker([
            ["username", None, "WORD"],
            ["password", None, "WORD"],
            ["phone", None, "NUMBER"],
            ["gender", "female"],
            ["email", None, "EMAIL"]
        ]).check(target)
        logger.debug("all_match res {}".format(res))
    except CheckFailed as check_err:
        logger.error("all_match err {}".format(check_err))

def test_custom_regex():
    target = {
        "username": "dlwxxxdlw",
        "password": "zxvxcgweg",
        "phone": "1234567890",
        "email": "heheeheheda@gmail.com"
    }

    try:
        res = Checker([
            ["username", None, "WORD"],
            ["password", None, "WORD"],
            ["phone", None, re.compile('^(138|181)').match],
            ["gender", "female"],
            ["email", None, "EMAIL"]
        ]).check(target)
        logger.debug("custom_regex res {}".format(res))
    except CheckFailed as check_err:
        logger.error("custom_regex err {}".format(check_err))

def test_value_not_allowed():
    target = {
        "username": "dlwxxxdlw",
        "password": "zxvxcgweg",
        "phone": "1234567890",
        "gender": "female",
        "email": "heheeheheda@gmail.com"
    }

    try:
        res = Checker([
            ["username", None, "WORD"],
            ["password", None, "WORD"],
            ["phone", None, "NUMBER"],
            ["email", None, "EMAIL"]
        ]).check(target)
        logger.debug("value_not_allowed res {}".format(res))
    except CheckFailed as check_err:
        logger.error("value_not_allowed err {}".format(check_err))
