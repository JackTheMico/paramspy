![alt text](./title.GIF "Title")
# Paramspy -- Parameters Checker for Pythoner

## How To Use
```Python
from paramspy import Checker, CheckFailed
target = {
    "username": "dlwxxxdlw",
    "password": "zxvxcgweg",
    "phone": "1234567890%$^",
}
rules = [
    ("username", str, "WORD"),
    ("password", str, "WORD"],
    ("phone", int, "NUMBER"),
    ["gender", "female", ["female", "male", "secret"]]
]
res = Checker(rules).check(target)
```
In a word, the rules above will check if "username", "password", "phone", "gender" in 
target; and "username", "password" must be str type, also have to obey default rule: "WORD".
As for "phone", it must be an int type and obey default rule: "NUMBER".
For "gender", it must in range ["female", "male", "secret"].
If you look closely, you will notice "username", "password", "phone" rules are all in tuple type,
but "gender" rule is in a list. Well, this difference make gender optional, means if target don't
have a parameter named "gender", Checker will add it for you with default value "female".But for 
those rules in tuple type, if parameter not in target or parameter's value is empty, will raise 
CheckFailed.

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

