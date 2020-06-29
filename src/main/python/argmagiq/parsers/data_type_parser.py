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


import abc
import typing

import insanity

import argmagiq.value_spec as value_spec


__author__ = "Patrick Hohenecker"
__copyright__ = "Copyright (c) 2020, Patrick Hohenecker"
__license__ = "BSD-2-Clause"
__version__ = "0.1.0"
__date__ = "29 Jun 2020"
__maintainer__ = "Patrick Hohenecker"
__email__ = "patrick.hohenecker@gmx.at"
__status__ = "Development"


class DataTypeParser(metaclass=abc.ABCMeta):
    """An abstract base class for data-type specific arg parsers."""

    def __init__(self, spec: value_spec.ValueSpec):
        """Creates a new ``DataTypeParser`` for the provided :class:`value_spec.ValueSpec`.

        Args:
            spec (:class:`value_spec.ValueSpec`): The specification of the value to parse.
        """

        # sanitize args
        insanity.sanitize_type("spec", spec, value_spec.ValueSpec)

        # store args
        self._spec = spec

        # compute the name of the according command-line arg
        self._arg_name = self.translate_config_name(spec.name)

    #  PROPERTIES  #####################################################################################################

    @property
    def spec(self) -> value_spec.ValueSpec:
        """:class:`value_spec.ValueSpec`: The specification used by the ``DataTypeParser``."""

        return self._spec

    @property
    def synopsis(self) -> typing.Tuple[str, str]:
        """tuple[str, str]: The synopsis of the command-line arg handled by the ``DataTypeParser`` as a pair consisting
        of the command (e.g., ``"--some-arg VALUE"``) and the according help text.
        """

        cmd = f"{self._arg_name} VALUE"
        description = self._spec.description
        if self._spec.default_value is not None:
            description += f" (Default value: {self._spec.default_value})"

        return cmd, description

    #  METHODS  ########################################################################################################

    @staticmethod
    def translate_config_name(name: str) -> str:
        """Translates the name of a configuration to the name of the according command-line arg.

        Args:
            name (str): The name of the configuration.

        Returns:
            str: The name of the according command-line arg.
        """

        return "--" + name.lower().replace("_", "-")

    @abc.abstractmethod
    def _parse(self, argv: typing.Tuple[str, ...]) -> typing.Tuple[typing.Any, typing.Tuple[str, ...]]:
        """This is the actual implementation of :meth:`parse`, which is invoked after sanitizing args."""

    def fires(self, argv: typing.Tuple[str, ...]) -> bool:
        """Evaluates whether the ``DataTypeParser`` should be used to parse the next args (at the beginning of the
        provided ``tuple``). To that end, parsers fire based on the name of the first arg only, which means that this
        method does not account for any subsequent args. Instead, :meth:`parse` (actually :meth:_parse) should raise an
        appropriate error, if any subsequent args are missing or invalid.

        Args:
            argv (tuple[str]): The remaining args to parse.

        Returns:
            bool: ``True`` iff the ``DateTypeParser`` should be used.
        """

        # sanitize args
        insanity.sanitize_type("argv", argv, tuple)
        insanity.sanitize_iterable("argv", argv, elements_type=str)

        # determine whether the parser fires
        return len(argv) > 0 and argv[0] == self._arg_name

    def parse(self, argv: typing.Tuple[str, ...]) -> typing.Tuple[typing.Any, typing.Tuple[str, ...]]:
        """Parses the next arg in the provided tuple of command-line args.

        Args:
            argv (tuple[str]): The remaining args to be parsed.

        Returns:
            value: The parsed value.
            argv (tuple[str]): The remaining args that have not been consumed by the ``DataTypeParser``.

        Raises:
            ValueError: If the ``DataTypeParser`` does not fire for the (beginning of the) provided args, or if an error
                occurred during parsing.
        """

        # sanitize args + ensure that the parser actually fires
        if not self.fires(argv):
            raise ValueError("The parser does not fire for the provided args")

        # parse the args
        return self._parse(argv)

    def parse_json(self, json_value: typing.Any) -> typing.Any:
        """Parses a value that has been read from a JSON file by means of Python's ``json`` package.

        The default implementation only checks whether the provided value is of the required data type, and raises a
        ``TypeError``, if this is not the case.

        Args:
            json_value: A value from a configuration file that has been parsed by means of Python's ``json`` package.

        Returns:
            The parsed value.

        Raises:
            TypeError: If ``json_value`` is of an unsupported type.
            ValueError: If any other error occurred during parsing.
        """

        if isinstance(json_value, self._spec.data_type):
            return json_value
        else:
            raise TypeError(f"Invalid JSON value for configuration {self._spec.name}: {json_value}")
