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


import typing

import insanity


__author__ = "Patrick Hohenecker"
__copyright__ = "Copyright (c) 2020, Patrick Hohenecker"
__license__ = "BSD-2-Clause"
__version__ = "0.1.0"
__date__ = "29 Jun 2020"
__maintainer__ = "Patrick Hohenecker"
__email__ = "patrick.hohenecker@gmx.at"
__status__ = "Development"


class ValueSpec(object):
    """Describes a single value that is part of a configuration to be parsed, as specified by an instance of
    :class:`argmagiq.config_spec.ConfigSpec`..
    """

    def __init__(
            self,
            name: str,
            description: str,
            data_type: type,
            required: bool,
            default_value: typing.Any
    ):
        """Creates a new instance of ``ConfigValue``.

        Args:
            Cf. the documentation of the according properties.

        Raises:
            ValueError: If ``data_type`` is ``bool`` and ``default_value`` is ``None``.
        """

        # sanitize args
        name = str(name)
        if not name:
            raise ValueError("<name> cannot be the empty string")
        description = str(description)
        insanity.sanitize_type("data_type", data_type, type)
        if data_type == bool and default_value is None:
            raise ValueError("For <data_type> bool, a default value is required")
        required = bool(required)

        # store args
        self._data_type = data_type
        self._default_value = default_value
        self._description = description
        self._name = name
        self._required = required

    #  MAGIC FUNCTIONS  ################################################################################################

    def __eq__(self, other: typing.Any) -> bool:

        return (
                isinstance(other, ValueSpec) and
                self._data_type is other.data_type and
                self._default_value == other.default_value and
                self._description == other.description and
                self._name == other.name and
                self._required == other.required
        )

    def __hash__(self):

        return hash(str(self))

    def __str__(self) -> str:

        return (
                f"ValueSpec(\n"
                f"    name          = \"{self._name}\",\n"
                f"    description   = \"{self._description}\",\n"
                f"    data_type     = {self._data_type},\n"
                f"    default_value = {self._default_value},\n"
                f"    required      = {self._required}\n"
                f")"
        )

    #  PROPERTIES  #####################################################################################################

    @property
    def data_type(self) -> type:
        """type: The data type of the specified configuration value."""

        return self._data_type

    @property
    def default_value(self) -> typing.Any:
        """The default value of the specified configuration value, which may be ``None``."""

        return self._default_value

    @property
    def description(self) -> str:
        """str: A description of the specified configuration value."""

        return self._description

    @property
    def name(self) -> str:
        """str: The name of the specified configuration value."""

        return self._name

    @property
    def required(self) -> bool:
        """bool: Indicates whether the specified configuration value has to be provided by a user."""

        return self._required
