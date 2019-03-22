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

## Now, let me explain it for you
    There are two types of rule:
      1. List, example:  ["gender", "female", ["female", "male", "secret"]].
         This means "gender" is a optional parameter, if the target you gonna check don't
         have a "gender" parameter, Checker will help you add it with a default value 
         , in this case is "female".
         And this ["female", "male", "secret"] means value have to be in these three values,
         if gender's value is "alien", Checker will raise CheckFailed Exception.

      2. tuple, example: ("phone", int, "NUMBER").
         This means parameter "phone" must be in the target which you about to check,
         if not, raise CheckFailed Exception.
         As for "int", it means type check, if a parameter is ok with multiple type, you
         can write it like: (int ,str, dict).
         Last one is a default rule, there are three default rules, you can take a look by
         calling Checker.default_rules() or just take a look in checker.py.
         
      3. You may already noticed, yes you can write lambda to implement some custom check logic.
         Also, Regular Expression is supported, for example:
          ["phone", None, (int, str), re.compile('^(138|181)')],
         Checker will use '^(138|181)' as pattern and re.match method to check the "phone"
         parameter's value.

### Default Rules for now:
```Python
    {
    'EMAIL': re.compile('^[a-z_0-9.-]{1,64}@([a-z0-9-]{1,200}.){1,5}[a-z]{1,6}$'),
    'NUMBER': re.compile('^[-+]?[0-9]+$'),
    'WORD': re.compile('[a-zA-Z-_\\d]+')
    }
``` 

### So, that's basicially all of it.
### Oh, One last thing, the Checker can check something like [{}, {}, {}] or a single dict object.
### I'm still considering if there is need or not to make a Object Checker.

#### By the way, if you found out that this README has many grammatical mistakes, 
#### that's because I'm a Chinese Programmer, I have few chance to communicate someone with English, but
#### I'm a big fan of "The Big Bang Theory" and "Rich and Morty" and extra.
## Thank you for you reading.
