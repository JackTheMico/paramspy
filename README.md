![alt text](./title.GIF "Title")
# Paramspy -- Parameters Checker for Pythoner

## How To Use
```Python
from paramspy import Checker, CheckFailed
from logging import getLogger

logger = getLogger(__name__)

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
        "gender": "alian"
    },
    {
        "username": "dlwxxxdlw",
        "password": "zxvxcgweg",
        "phone": "18934554354",
        "age": "35"
    },
    {
        "username": "dlwxxxdlw",
        "password": "zxvxcgweg",
        "phone": "18934554354",
        "age": 12
    },
]
try:
    res = Checker([
        ("username", str, "WORD"),
        ("password", str, "WORD"),
        ("phone", int, "NUMBER"),
        ["gender", "female", ["female", "male", "secret"]],
        ["age", None, (int,), lambda x: int(x) > 18]
    ]).check(target)
except CheckFailed as check_err:
    logger.error("{}".format(check_err))
    logger.error("error string \n{}".format(check_err.get_excstr()))
```

### Result
```Python
    [RuleNotMatch('index: 0, parameter: phone, value: 1234567890%$^ not match its rule: ^[-+]?[0-9]+$'), 
    RuleNotMatch('index: 1, parameter: username, value:  not match its rule: [a-zA-Z-_\\d]+'), 
    RuleNotMatch('index: 1, parameter: phone, value: 1234567890%$^ not match its rule: ^[-+]?[0-9]+$'), 
    RuleNotMatch("index 1, parameter: gender, value: alian not match its rule: ['female', 'male', 'secret']"), 
    TypeNotMatch("index: 2, parameter: age type <class 'str'>, value 35 not type (<class 'int'>,)"), 
    RuleNotMatch('index 3, parameter: age, value: 12 not match its rule: lambda x: int(x) > 18')]

    error string
    index: 0, parameter: phone, value: 1234567890%$^ not match its rule: ^[-+]?[0-9]+$
    index: 1, parameter: username, value:  not match its rule: [a-zA-Z-_\d]+
    index: 1, parameter: phone, value: 1234567890%$^ not match its rule: ^[-+]?[0-9]+$
    index 1, parameter: gender, value: alian not match its rule: ['female', 'male', 'secret']
    index: 2, parameter: age type <class 'str'>, value 35 not type (<class 'int'>,)
    index 3, parameter: age, value: 12 not match its rule: lambda x: int(x) > 18
```
    In a word, the rules above will check if "username", "password", "phone", "gender" in 
    target; and "username", "password" must be str type, also have to obey default rule: "WORD".

    As for "phone", it must be an int type and obey default rule: "NUMBER".

    For "gender", it must in range ["female", "male", "secret"].

    If you look closely, you will notice "username", "password", "phone" rules are all in tuple type,
    but "gender" rule is in a list. 

    Well, this difference make gender optional, means if target don't have a parameter named "gender", 
    Checker will add it for you with default value "female".

    But for those rules in tuple type, if parameter not in target or parameter's value is empty, 
    Checker will raise CheckFailed.

### ("username", str, "WORD") 
    This rule means target must have a parameter called "username" ,
    and its value cannot be empty, and value' type must be str.

    There are several default rules in Checker class, you can view it
    by call Checker.default_rules(). You will get something like:
```Python
{'EMAIL': re.compile('^[a-z_0-9.-]{1,64}@([a-z0-9-]{1,200}.){1,5}[a-z]{1,6}$'),
 'NUMBER': re.compile('^[-+]?[0-9]+$'),
 'WORD': re.compile('[a-zA-Z-_\\d]+')}
```
    If you don't want any type assert or rules, you can just use "username" as a rule like:
```Python
rules = [
    "username",
    ("password", str, "WORD"],
    ("phone", int, "NUMBER"),
    ["gender", "female", ["female", "male", "secret"]]
]
```

