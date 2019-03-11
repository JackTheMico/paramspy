# -*- coding:utf-8 -*-
"""
-------------------------------------------------

    File Name:        /Users/jackdeng/code/Python/paramspy/paramspy.py

    Description:      Python parameters check for Human

    Author:           dlwxxxdlw@gmail.com

    Date:             2019-03-07-16:07:49

    Version:          v1.0

    Lastmodified:     2019-03-07 by Jack Deng

-------------------------------------------------
"""

import re

try:
    from inspect import signature
except ImportError:
    from funcsigs import signature
from functools import wraps


def typeassert(*ty_args, **ty_kwargs):
    def decorate(func):
        # If in optimized mode, disable type checking
        if not __debug__:
            return func

        # Map function argument names to supplied types
        sig = signature(func)
        bound_types = sig.bind_partial(*ty_args, **ty_kwargs).arguments

        @wraps(func)
        def wrapper(*args, **kwargs):
            bound_values = sig.bind(*args, **kwargs)
            for name, value in bound_values.arguments.items():
                if name == "self":
                    continue
                if isinstance(bound_types[name], list):
                    assert_flag = False
                    for assert_type in bound_types[name]:
                        if isinstance(value, assert_type):
                            assert_flag = True
                            break
                    if not assert_flag:
                        raise TypeError(
                            'Argument {} must be {}'.format(name, bound_types[name])
                        )
                    continue
                if name in bound_types:
                    if not isinstance(value, bound_types[name]):
                        raise TypeError(
                            'Argument {} must be {}'.format(name, bound_types[name])
                        )
            return func(*args, **kwargs)
        return wrapper
    return decorate


class CheckFailed(Exception):
    """
    class CheckFailed for parameters check failed
    """

    def __init__(self, message):
        super(CheckFailed, self).__init__(message)


class RuleNotMatch(Exception):
    """
    class RuleNotMatch for regex rule not match
    """
    def __init__(self, message):
        super(RuleNotMatch, self).__init__(message)


class ParamNotAllow(Exception):
    """
    raising when some values which are not allowed by the rules
    """

    def __init__(self, message):
        super(ParamNotAllow, self).__init__(message)

class RuleNotFound(Exception):
    """
    class RuleNotFound for not found rule
    """
    def __init__(self, message):
        super(RuleNotFound, self).__init__(message)


class Checker(object):
    """
    class Checker for check parameters
    """

    default_rules = {
        "NUMBER": re.compile(r'^[-+]?[0-9]+$'),
        "WORD": re.compile(r'[a-zA-Z-_\d]+'),
        "EMAIL": re.compile(r'^[a-z_0-9.-]{1,64}@([a-z0-9-]{1,200}.){1,5}[a-z]{1,6}$')
    }



    @typeassert(rules=list)
    def __init__(self, rules):
        ""
        self.re_type = type(re.compile(''))
        self._rule_dict = {}
        for index, rule in enumerate(rules):
            if isinstance(rule ,list):
                self._rule_dict[rule[0]] = rule[1:]
            elif isinstance(rule, str):
                self._rule_dict[rule] = None
            else:
                raise TypeError(
                    'rule {} must be a str or a list'.format(index)
                )

    @typeassert(data=[list, dict])
    def check(self, data):
        exc_list = []
        if isinstance(data, dict):
            data = [data]
        for each in data:
            self.__check(exc_list, each)
        if len(exc_list) > 0:
            raise CheckFailed(exc_list)
        if len(data) == 1:
            return data[0]
        return data

    @typeassert(exclist=list, target=dict)
    def __check(self, exclist, target):
        for key, val in target.items():
            if key not in self._rule_dict.keys():
                exclist.append(ParamNotAllow(
                    'parameter: {} not allowed, value: {}'.format(key, val)
                ))
                continue
            elif key in self._rule_dict.keys():
                rule_val = self._rule_dict[key]
                if not rule_val:
                    continue
                if not val:
                    val = rule_val[0]
                elif val and len(rule_val) > 1:
                    rule = rule_val[-1]
                    if isinstance(rule, self.re_type):
                        judge = rule.match(val)
                        if judge:
                            continue
                        exclist.append(RuleNotMatch(
                            'parameter: {}, value: {} not match its rule: {}'.format(
                                key, val, rule.pattern)
                        ))
                    elif isinstance(rule, str):
                        if rule not in self.default_rules.keys():
                            exclist.append(RuleNotFound(
                                "not found parameter: {}'s rule: {}".format(key, rule)
                            ))
                            continue
                        try:
                            judge = self.default_rules[rule].match(val)
                        except TypeError:
                            pre_type = type(val)
                            judge = self.default_rules[rule].match(str(val))
                            val = pre_type(val)
                        if judge:
                            continue
                        exclist.append(RuleNotMatch(
                            'parameter: {}, value: {} not match its rule: {}'.format(
                                key, val, self.default_rules[rule].pattern)
                        ))
                    elif isinstance(rule, list) or isinstance(rule, tuple):
                        if val in rule:
                            continue
                        exclist.append(RuleNotMatch(
                            'parameter: {}, value: {} not match its rule: {}'.format(
                                key, val, rule)
                        ))
        for rule_key, rule_val in self._rule_dict.items():
            if rule_key not in target.keys():
                if rule_val and len(rule_val) > 0:
                    target[rule_key] = rule_val[0]


class ObjChecker(object):
    """
    Checker for Object
    """

    @typeassert(rules=dict)
    def __init__(self, rules):
        "init check rules"
        self._rule_dict = {}
        for key, val in rules.items():
            if key == "basic":
                self._rule_dict["basic"] = val
            self._rule_dict[key.__name__] = val

    @typeassert(data=[list, dict])
    def check(self, data):
        """
        check logic
        :Keyword Arguments:
         self --
         data --
        :return: checked and maybe modified data
        """


