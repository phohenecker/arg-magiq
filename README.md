arg-magiq
=========


`argmagiq` is a Python library that allows for parsing command-line args automagically.
To that end, all you have to do is to define a configuration class that contains a property for each of the user-defined
args, and let `argmagiq` take care of parsing them for you



Installation
------------


The package `argmagiq` can be installed via pip as follows:

```bash
pip install git+https://github.com/phohenecker/arg-magiq
```



How-To
------


### Step 1: Define Your Config Class

Every property (**not** attribute) of your configuration class that has both a getter **and** a setter method is
considered as an arg.
Please notice that all args are treated as options, i.e., `argmagiq` does not generate positional args, and the name of
a considered property `my_property` is translated into an according option `--my-property`.
For example, the following code defines an arg ``--my-property``:

```python
@property
def my_property(self) -> str:
    """str: This property defines an arg."""
    return self._my_property

@my_property.setter
def my_property(self, my_property: str) -> None:
    self._my_property = my_property
```

An important detail of this code snippet is the **return-type annotation** of the getter method, which allows `argmagiq`
to identify the data type of the according arg and sanitize values provided by the user.
At the moment, the types `bool`, `int`, `float`, and `str` are supported.
Notice that generic type-aliases are not allowed except for `typing.Optional[X]`, if `X` is any of the supported types. 
Finally, notice that the docstring of the getter method, if present, is printed as description of the arg in the help
text of the application.

**Notice:**
Just like Python's `argparse` package, `argmagiq` prints an automatically generated help text, if either `-h` or
`--help` is provided.


### Step 2: Let `argmagiq` Parse Args

Once you defined your config class, parsing args is as easy as importing `argmagiq` and running a single command:

```python
import argmagiq

parsed_config = argmagiq.parse_args(
        YourConfigClass,
        app_name,
        app_description
)
```

In this code snippet, `app_name` and `app_description` are two strings that define the name of your application, which
is used in its synopsis (the usage instruction at the beginning of the help), as well as a description of the same,
which is displayed as part of the help text.
The return value of `parse_args` is an instance of `YourConfigClass` that has been populated with the values provided
for the corresponding args.

**Notice:**
When the help text is printed (i.e., the user provided `-h` or `--help`), then `parse_args` returns `None`.


### Default Values

If an arg has a default value, then this has to be specified as an attribute of the config class.
The name of such an attribute has to be an all-caps version of the according property prefixed with `DEFAULT_`.
For example, the following snippet defines a default value for the property `my_property` (which, as before, defines the
arg `--my-property`):

```python
class YourConfigClass(object):

    DEFAULT_MY_PROPERTY = "blub"
    ...
```

By default, every arg without default value is considered as required, and an error will be raised, if the user does not
specify the same.
If you want to explicitly mark an arg without default value as optional, though, then you can annotate the
according getter method with `@argmagiq.optional`:

```python
@argmagiq.optional
@property
def my_property(self) -> str:
    ...
```


### Reading Args From A JSON File

As an alternative way of specifying args, which is particularly handy, if an applications requires a lot of
user-defined configuration, `argmagiq` allows for providing them as a JSON file as follows:

```bash
$ ./your-app.py -- /path/to/config.json
```

In this example, the file at path `/path/to/config.json` specifies the args for the application.
Notice that JSON files have to be shallow dictionaries that describe key-value pairs using the same naming as the
configuration class.
For example:

```json
{
    "my_property": "some value",
    ...
}
```



Examples
--------


For full working examples, please have a look at the
[`examples` folder](https://github.com/phohenecker/arg-magiq/tree/master/examples).
