# -*- coding: utf-8 -*-

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                                                     #
#   BSD 2-Clause License                                                              #
#                                                                                     #
#   Copyright (c) 2020, Patrick Hohenecker                                            #
#   All rights reserved.                                                              #
#                                                                                     #
#   Redistribution and use in source and binary forms, with or without                #
#   modification, are permitted provided that the following conditions are met:       #
#                                                                                     #
#   1. Redistributions of source code must retain the above copyright notice, this    #
#      list of conditions and the following disclaimer.                               #
#                                                                                     #
#   2. Redistributions in binary form must reproduce the above copyright notice,      #
#      this list of conditions and the following disclaimer in the documentation      #
#      and/or other materials provided with the distribution.                         #
#                                                                                     #
#   THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"       #
#   AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE         #
#   IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE    #
#   DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE      #
#   FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL        #
#   DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR        #
#   SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER        #
#   CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,     #
#   OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE     #
#   OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.              #
#                                                                                     #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


import inspect
import re
import typing

import insanity

import argmagiq
import argmagiq.value_spec as value_spec


__author__ = "Patrick Hohenecker"
__copyright__ = "Copyright (c) 2020, Patrick Hohenecker"
__license__ = "BSD-2-Clause"
__version__ = "0.1.0"
__date__ = "29 Jun 2020"
__maintainer__ = "Patrick Hohenecker"
__email__ = "patrick.hohenecker@gmx.at"
__status__ = "Development"


class ConfigSpec(object):
    """A specification of a collection of configuration values that have to be parsed."""

    DOC_REGEX = r"^([A-Za-z0-9_]+:\s+)?(?P<doc>.*)"
    """str: A regex for removing the (optional) type specification from properties' docstrings."""

    #  CONSTRUCTOR  ####################################################################################################

    def __init__(self):
        """Creates a new empty ``ConfigSpec``."""

        # create the (empty) list of config values
        self._config_values = []

    #  MAGIC FUNCTIONS  ################################################################################################

    def __eq__(self, other: typing.Any) -> bool:

        return (
                isinstance(other, ConfigSpec) and
                len(self) == len(other) and
                all(other.get_value_by_name(x.name) == x for x in self._config_values)
        )

    def __iter__(self) -> typing.Iterator[value_spec.ValueSpec]:

        return iter(self._config_values)

    def __len__(self) -> int:

        return len(self._config_values)

    #  METHODS  ########################################################################################################

    def add_value(self, spec: value_spec.ValueSpec) -> None:
        """Adds a configuration value to the ``ConfigSpec``.

        Args:
            spec (:class:`value_spec.ValueSpec`): The specification of the configuration value to add.
        """

        insanity.sanitize_type("spec", spec, value_spec.ValueSpec)
        self._config_values.append(spec)

    def get_value_by_name(self, name: str) -> typing.Optional[value_spec.ValueSpec]:
        """Retrieves the specification of the configuration value with the provided name, if it exists.

        Args:
            name (str): The name of the configuration to retrieve.

        Returns:
            :class:`value_spec.ValueSpec`: The specification or ``None``, if there is no configuration with the provided
                ``name``.
        """

        for spec in self._config_values:
            if spec.name == name:
                return spec

        return None

    @classmethod
    def create_from(cls, config_cls: type):
        """A factory method for creating a configuration specification based on the provided class.

        The created specification defines one option for each property (i.e., methods annotated with ``@property``) of
        the given class except those that start with an underscore (i.e., private properties). Class-level fields whose
        names start with :attr:`argmagiq.DEFAULT_PREFIX` are assumed to define default values for options. Type and
        description for each of the options are extracted from the according property's type annotations and
        docstring.

        Args:
            config_cls (type): The class that the configuration is based on.
        """

        spec = ConfigSpec()

        # load all default values
        default_values = {}
        for name, field in inspect.getmembers(config_cls, lambda f: not inspect.isroutine(f)):
            if name.startswith(argmagiq.DEFAULT_PREFIX):
                field_name = name[len(argmagiq.DEFAULT_PREFIX):].lower()
                default_values[field_name] = field

        # find all public mutable properties -> these are considered as config values
        for name, field in inspect.getmembers(config_cls, lambda f: isinstance(f, property)):

            # only consider public properties that have an according setter method
            if name.startswith("_") or field.fset is None:
                continue

            # check if the config has a default value specified
            default_value = None
            if name in default_values:
                default_value = default_values[name]

            # check if the option is required
            required = (
                    default_value is None and
                    not (argmagiq.OPTIONAL_KEY in field.fget.__dict__)
            )

            # fetch docstring as description of the config
            if field.__doc__ is None:
                description = "No description available."
            else:
                m = re.match(cls.DOC_REGEX, field.__doc__)  # -> this is done to remove any type specifications
                description = m.group("doc") if m else "No description available."

            # determine the option's data type from the properties type annotation
            sig = inspect.signature(field.fget)
            if sig.return_annotation is None:
                raise ValueError(f"Property <{name}> does not have a return-type annotation")
            data_type = sig.return_annotation

            # if the datatype is a generic alias, then we have to extract the actual data type from it
            if not isinstance(data_type, type):  # -> the type is a generic alias

                # check if the data type is a union
                # -> this also covers typing.Optional[X], which is a shorthand for typing.Union[X, None]
                if "__origin__" in data_type.__dict__ and data_type.__dict__["__origin__"] == typing.Union:

                    # gather all types in the union except None
                    all_types = [t for t in data_type.__dict__["__args__"] if t is not type(None)]

                    # ensure that there is just one type left
                    if len(all_types) == 1:
                        data_type = all_types[0]
                    else:
                        raise ValueError(f"Property <{name}> has an ambiguous data type")

                else:

                    # since no other generic aliases are supported, raise an error
                    raise ValueError(f"Property <{name}> has an unsupported generic-alias type: {data_type}")

            # add the parsed information to the config spec
            spec.add_value(
                    value_spec.ValueSpec(name, description, data_type, required, default_value)
            )

        return spec
