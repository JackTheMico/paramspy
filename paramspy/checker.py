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
    from inspect import getsourcelines
except ImportError:
    from funcsigs import getsourcelines
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

    def get_excstr(self):
        res_str = ""
        for err in self.args[0]:
            res_str += "".join([err.__str__(), "\n"])
        return res_str


class RuleNotMatch(Exception):
    """
    class RuleNotMatch for regex rule not match
    """
    def __init__(self, message):
        super(RuleNotMatch, self).__init__(message)

class TypeNotMatch(Exception):
    """
    class TypeNotMatch for type not match
    """


class ParamNotAllow(Exception):
    """
    raising when some values which are not allowed by the rules
    """

    def __init__(self, message):
        super(ParamNotAllow, self).__init__(message)

class ParamNotFound(Exception):
    """
    raising when some values which are not Founded by the rules
    """

    def __init__(self, message):
        super(ParamNotFound, self).__init__(message)


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

    _default_rules = {
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
            elif isinstance(rule, tuple):
                if len(rule) == 1:
                    self._rule_dict[rule[0]] = tuple()
                elif len(rule) < 1:
                    raise TypeError(
                        'rule cannot be a empty tuple'
                    )
                else:
                    self._rule_dict[rule[0]] = rule[1:]
            elif isinstance(rule, str):
                self._rule_dict[rule] = None
            else:
                raise TypeError(
                    'rule {} must be a str or a list or a tuple'.format(index)
                )

    @typeassert(data=[list, dict], raise_first=bool)
    def check(self, data, raise_first=False):
        exc_list = []
        if isinstance(data, dict):
            data = [data]
        for index, each in enumerate(data):
            self.__check(index, exc_list, each)
            if raise_first and len(exc_list) == 1:
                break
        if len(exc_list) > 0:
            raise CheckFailed(exc_list)
        if len(data) == 1:
            return data[0]
        return data

    @classmethod
    def default_rules(cls):
        from pprint import pprint
        pprint(cls._default_rules)
        return cls._default_rules

    @typeassert(index=int, exclist=list, target=dict)
    def __check(self, index, exclist, target):
        for key, val in target.items():
            if key not in self._rule_dict.keys():
                exclist.append(ParamNotAllow(
                    'index: {}, parameter: {} not allowed, value: {}'.format(
                        index, key, val)
                ))
                continue
            elif key in self._rule_dict.keys():
                rules = self._rule_dict[key]
                if isinstance(rules, tuple):
                    self.__rules_check_not_None(index, exclist, key, val, rules)
                elif isinstance(rules, list):
                    if not val:
                        val = rules[0]
                        continue
                    for rule in rules[1:]:
                        if isinstance(rule, str) \
                           or isinstance(rule, self.re_type) \
                           or isinstance(rule, list):
                            self.__rule_check(index, exclist, key, val, rule)
                        elif isinstance(rule, tuple):
                            self.__type_check(index, exclist, key, val, rule)
                        elif isinstance(rule, type(lambda:None)):
                            self.__lambda_check(index, exclist, key, val, rule)
                elif rules is None:
                    continue

        for rule_key, rule_val in self._rule_dict.items():
            if rule_key not in target.keys() and isinstance(rule_val, tuple):
                exclist.append(ParamNotFound(
                    'index {} rule define parameter {} not found'.format(index, rule_key)))
            elif rule_key not in target.keys() and isinstance(rule_val, list):
                target[rule_key] = rule_val[0]

    def __rules_check_not_None(self, index, exclist, key, val, rules):
        if len(rules) == 0:
            exclist.append(RuleNotFound(
                'index {}, parameter {}, value {} not found rule, \n \
                if don\'t need rule, please use str type'.format(
                        index, key, val)
            ))
            return
        for rule in rules:
            if isinstance(rule, str) \
               or isinstance(rule, self.re_type) \
               or isinstance(rule, list):
                self.__rule_check(index, exclist, key, val, rule)
            elif isinstance(rule, tuple):
                self.__type_check(index, exclist, key, val, rule)
            elif isinstance(rule, type(lambda:None)):
                self.__lambda_check(index, exclist, key, val, rule)

    def __get_funcstr(self, func):
        funcstring = str(getsourcelines(func)[0])
        func_str = funcstring.strip("['\\n']")
        func_str = func_str[func_str.index("lambda"):]
        return func_str

    def __lambda_check(self, index, exclist, key, val, lambda_rule):
        if not lambda_rule(val):
            exclist.append(RuleNotMatch(
                'index {}, parameter: {}, value: {} not match its rule: {}'.format(
                    index, key, val, self.__get_funcstr(lambda_rule))
            ))

    def __type_check(self, index, exclist, key, val, type_rules):
        if isinstance(type_rules, tuple):
            if type(val) not in type_rules:
                exclist.append(TypeNotMatch(
                    'index: {}, parameter: {} type {}, value {} not type {}'.format(
                        index, key, type(val), val, type_rules)
                ))
        else:
            if not isinstance(val, type_rules):
                exclist.append(TypeNotMatch(
                    'index: {}, parameter: {} type {}, value {} not type {}'.format(
                        index, key, type(val), val, type_rules)
                ))

    def __rule_check(self, index, exclist, key, val, match_rule):
        if isinstance(match_rule, str):
            if match_rule not in self._default_rules.keys():
                exclist.append(RuleNotFound(
                    "index: {}, not found parameter: {}'s rule: {}".format(key, rule)
                ))
                return
            default_re = self._default_rules[match_rule]
            try:
                judge = default_re.match(val)
            except TypeError:
                pre_type = type(val)
                judge = default_re.match(str(val))
                val = pre_type(val)
            if not judge:
                exclist.append(RuleNotMatch(
                    'index: {}, parameter: {}, value: {} not match its rule: {}'.format(
                        index, key, val, default_re.pattern)
                ))
        elif isinstance(match_rule, self.re_type):
            try:
                judge = match_rule.match(val)
            except TypeError:
                pre_type = type(val)
                judge = match_rule.match(str(val))
                val = pre_type(val)
            if not judge:
                exclist.append(RuleNotMatch(
                    'index: {}, parameter: {}, value: {} not match its rule: {}'.format(
                        index, key, val, match_rule.pattern)
                ))
        elif isinstance(match_rule, list) or isinstance(match_rule, tuple):
            if val not in match_rule:
                exclist.append(RuleNotMatch(
                    'index {}, parameter: {}, value: {} not match its rule: {}'.format(
                        index, key, val, match_rule)
                ))


class ObjChecker(object):
    """
    Checker for Object attributes
    TODO not finished yet, still working on this one
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
        pass

