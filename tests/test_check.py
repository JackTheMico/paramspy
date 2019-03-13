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

from paramspy import (
    Checker,
    CheckFailed,
    RuleNotMatch,
    TypeNotMatch,
    ParamNotFound
)

# tuple means no dafault value, the value must come from input data
# (param, type, rule)
# (param, rule)
# if no param in input data, will use default_value for param
# [param, default_value, type, rule]
# [param, default_value, type]
# [param, default_value, rule]


def test_not_match():
    target = [
        {
            "username": "dlwxxxdlw",
            "password": "zxvxcgweg",
            "phone": "1234567890%$^",
        },
        {
            "username": "",
            "password": "zxvxcgweg",
            "phone": "1234567890%$^",
        },
    ]

    try:
        res = Checker([
            ("username", str, "WORD"),
            ["password", None, "WORD"],
            ("phone", int, "NUMBER"),
            ["gender", "female"]
        ]).check(target)
    except CheckFailed as check_err:
        assert isinstance(check_err.args[0][0], TypeNotMatch)
        assert isinstance(check_err.args[0][1], RuleNotMatch)
        logger.error("{}".format(check_err))
        logger.warning("default rules {}".format(Checker.default_rules()))

    try:
        res = Checker([
            ["username", None, "WORD"],
            ["password", None, "WORD"],
            ("phone", "NUMBER"),
            ["gender", "female"]
        ]).check(target)
    except CheckFailed as check_err:
        assert isinstance(check_err.args[0][0], RuleNotMatch)
        logger.error("{}".format(check_err))


def test_param_not_found_value():
    target = {
        "username": "dlwxxxdlw",
        "password": "zxvxcgweg",
    }
    try:
        res = Checker([
            ["username", None, "WORD"],
            ["password", None, "WORD"],
            ("phone", "NUMBER"),
            ["gender", "female"]
        ]).check(target)
    except CheckFailed as check_err:
        assert isinstance(check_err.args[0][0], ParamNotFound)
        logger.error("{}".format(check_err))

def test_default_value():
    target = {
        "username": "dlwxxxdlw",
        "password": "zxvxcgweg",
    }
    target1 = {
        "username": "dlwxxxdlw",
        "password": "zxvxcgweg",
        "gender": "alien"
    }
    try:
        res = Checker([
            ["username", None, "WORD"],
            ["password", None, "WORD"],
            ["gender", "female"]
        ]).check(target)
        logger.debug(res)
        res1 = Checker([
            ["username", None, "WORD"],
            ["password", None, "WORD"],
            ["gender", "female", str, ["male", "female"]]
        ]).check(target1)
    except CheckFailed as check_err:
        logger.error("{}".format(check_err))


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
            ["phone", None, int,"NUMBER"],
            ("gender", ["female", "male"]),
            ["email", None, "EMAIL"]
        ]).check(target)
    except CheckFailed as check_err:
        logger.error(check_err)

def test_all_match():
    target = {
        "username": "dlwxxxdlw",
        "password": "zxvxcgweg",
        "phone": 1234567890,
        "email": "heheeheheda@gmail.com"
    }

    try:
        res = Checker([
            ["username", None, "WORD"],
            ["password", None, "WORD"],
            ["phone", None, int,"NUMBER"],
            ["gender", "female"],
            ["email", None, "EMAIL"]
        ]).check(target)
        logger.debug(res)
    except CheckFailed as check_err:
        logger.error(check_err)

def test_custom_regex():
    target = [
        {
            "username": "dlwxxxdlw",
            "password": "zxvxcgweg",
            "phone": 13889232341,
            "email": "heheeheheda@gmail.com"
        },
        {
            "username": "dlwxxxdlw",
            "password": "zxvxcgweg",
            "phone": "1234567890",
            "email": "heheeheheda@gmail.com"
        },
    ]

    try:
        res = Checker([
            ["username", None, "WORD"],
            ["password", None, "WORD"],
            ["phone", None, [int, str],re.compile('^(138|181)')],
            ["gender", "female"],
            ["email", None, "EMAIL"]
        ]).check(target)
        logger.debug(res)
    except CheckFailed as check_err:
        logger.error(check_err)

def test_custom_list_rule():
    target = [
        {
            "username": "dlwxxxdlw",
            "password": "zxvxcgweg",
            "phone": 12345456790,
            "gender": "male",
            "email": "heheeheheda@gmail.com"
        },
        {
            "username": "dlwxxxdlw",
            "password": "zxvxcgweg",
            "phone": "12345456790",
            "gender": "alien",
            "email": "heheeheheda@gmail.com"
        }
    ]

    try:
        res = Checker([
            ["username", None, "WORD"],
            ["password", None, "WORD"],
            ["phone", None, (int,)],
            ["gender", None, ["female", "male", "secret"]],
            ["email", None, "EMAIL"]
        ]).check(target)
        logger.debug("{}".format(res))
    except CheckFailed as check_err:
        logger.error("{}".format(check_err))

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
            ("username", str, "WORD"),
            ("password", str, "WORD"),
            ("phone", int, "NUMBER"),
            ["email", None, "EMAIL"]
        ]).check(target)
        logger.debug("{}".format(res))
    except CheckFailed as check_err:
        logger.error("{}".format(check_err))

def test_list_data():
    target = [
        {
            "username": "dlwxxxdlw",
            "password": "zxvxcgweg",
            "phone": "1234567890",
            "gender": "female",
            "email": "heheeheheda@gmail.com"
        },
        {
            "username": "dlwxxxdlw",
            "phone": 1234567890,
            "gender": "female",
            "email": "heheeheheda@gmail.com"
        },
        {
            "username": 123456,
            "password": "zxvxcgweg",
            "phone": "1234567890",
            "email": "bademail"
        },
    ]

    try:
        res = Checker([
            ("username", str, "WORD"),
            ("password", str, "WORD"),
            ("phone", int, "NUMBER"),
            ["gender", "secret"],
            ("email", str, "EMAIL")
        ]).check(target)
        logger.debug("{}".format(res))
    except CheckFailed as check_err:
        logger.error("{}".format(check_err))


def test_no_rule():
    target = [
        {
            "username": "dlwxxxdlw",
            "password": "zxvxcgweg",
            "phone": "1234567890",
            "gender": "female",
            "email": "heheeheheda@gmail.com"
        },
        {
            "username": "dlwxxxdlw",
            "phone": 1234567890,
            "gender": "female",
            "email": "heheeheheda@gmail.com"
        },
        {
            "username": 123456,
            "password": "zxvxcgweg",
            "phone": "1234567890",
            "email": "bademail"
        },
    ]

    try:
        res = Checker([
            "username",
            "password",
            "phone",
            "gender",
            "email",
        ]).check(target)
        logger.debug("{}".format(res))
    except CheckFailed as check_err:
        logger.error("{}".format(check_err))
