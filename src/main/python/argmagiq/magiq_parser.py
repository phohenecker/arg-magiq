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
import json
import os
import re
import sys
import textwrap
import typing

import insanity

import argmagiq
import argmagiq.config_spec as config_spec
import argmagiq.parsers.bool_parser as bool_parser
import argmagiq.parsers.data_type_parser as data_type_parser
import argmagiq.parsers.float_parser as float_parser
import argmagiq.parsers.int_parser as int_parser
import argmagiq.parsers.str_parser as str_parser


__author__ = "Patrick Hohenecker"
__copyright__ = "Copyright (c) 2020, Patrick Hohenecker"
__license__ = "BSD-2-Clause"
__version__ = "0.1.0"
__date__ = "29 Jun 2020"
__maintainer__ = "Patrick Hohenecker"
__email__ = "patrick.hohenecker@gmx.at"
__status__ = "Development"


class MagiqParser(object):
    """This class implements the actual parsing procedure."""

    #  CONSTRUCTOR  ####################################################################################################

    def __init__(
            self,
            spec: type,
            app_name: str,
            app_description: str
    ):
        """Creates a new instance of ``MagiqParser``.

        Args:
            spec (type): A configuration class that specifies how to parse args.
            app_name (str): The name of the application whose args are being parsed. This is printed in the help text.
            app_description (str): A description of the application whose args are being parsed. This is printed in the
                help text.
        """

        # sanitize args
        insanity.sanitize_type("spec", spec, type)
        if not inspect.isclass(spec):
            raise TypeError("<spec> has to be class")
        if len(inspect.signature(spec.__init__).parameters) != 1:  # -> 1 for self
            raise ValueError("<spec> has to have a no-arg constructor")
        app_name = str(app_name)
        app_description = str(app_description)

        # store args
        self._app_description = app_description
        self._app_name = app_name
        self._spec = spec

    #  METHODS  ########################################################################################################

    @staticmethod
    def _create_parsers(spec: config_spec.ConfigSpec) -> typing.List[data_type_parser.DataTypeParser]:
        """Creates all parsers required to parse a configuration of the provided spec.

        Args:
            spec (:class:`config_spec.ConfigSpec`): The spec that describes the configuration that needs to be parsed.

        Returns:
            list[:class:`data_type_parser.DataTypeParser`]: The created parsers.

        Raises:
            ValueError: If configuration values of an unsupported type are encountered in the ``spec``.
        """

        field_parsers = []
        for value_spec in spec:  # -> iterate over config values in the spec

            # create a parser for the currently considered config value
            if value_spec.data_type is bool:
                field_parsers.append(bool_parser.BoolParser(value_spec))
            elif value_spec.data_type is float:
                field_parsers.append(float_parser.FloatParser(value_spec))
            elif value_spec.data_type is int:
                field_parsers.append(int_parser.IntParser(value_spec))
            elif value_spec.data_type is str:
                field_parsers.append(str_parser.StrParser(value_spec))
            else:
                raise ValueError(
                        f"Unsupported type of property <{value_spec.name} in the configuration class: "
                        f"{value_spec.data_type}"
                )

        return field_parsers

    def _print_help_text(self, spec: config_spec.ConfigSpec) -> None:
        """Prints the help text to the screen."""

        # prepare the app description
        desc_pars = re.split("\\n\\n+", self._app_description)
        desc_pars = "\n\n".join("\n".join(textwrap.wrap(p.strip(), width=argmagiq.TEXT_WIDTH)) for p in desc_pars)

        # prepare the option description
        options = [p.synopsis for p in self._create_parsers(spec)]
        options.append(("--help (or -h)", "Show this help."))
        options.sort(key=lambda x: x[0])
        option_width = max(len(opt[0]) for opt in options)  # -> the width of the left column
        desc_width = argmagiq.TEXT_WIDTH - option_width - 2  # -> the width of the right column
        formatted_options = []
        for opt_syn, opt_desc in options:

            opt_desc = textwrap.wrap(opt_desc, width=desc_width)
            formatted_lines = [f"{opt_syn.ljust(option_width)}  {opt_desc[0]}"]
            for desc_line in opt_desc[1:]:
                formatted_lines.append(f"{' ' * option_width}  {desc_line}")
            formatted_options.append("\n".join(formatted_lines))

        formatted_options = "\n".join(formatted_options)

        print(
                (
                        f"\n"
                        f"{desc_pars}\n"
                        f"\n"
                        f"Usage: {self._app_name} [OPTION]...\n"
                        f"  or   {self._app_name} -- FILE_PATH\n"
                        f"\n"
                        f"Options:\n"
                        f"{formatted_options}\n"
                )
        )

    @classmethod
    def _read_args_from_command_line(
            cls,
            spec: config_spec.ConfigSpec,
            argv: typing.Tuple[str, ...]
    ) -> typing.Dict[str, typing.Any]:
        """Parses a tuple of command-line args into dictionary of configuration values.

        Args:
            spec (:class:`config_spec.ConfigSpec`): The spec that describes the configuration that needs to be parsed.
            argv (tuple[str]): The command-line args to parse.

        Returns:
            dict: The parsed configuration.

        Raises:
            ValueError: If an unknown arg is encountered or parsing any arg fails for some reason.
        """

        parsed_args = {}

        # create parsers for all config values
        field_parsers = cls._create_parsers(spec)

        # parse the args
        while argv:  # -> as long as there are args left

            # find a parser to use
            for fp in field_parsers:

                if fp.fires(argv):  # -> the parser can be used to parse the next option

                    # parse the currently considered arg
                    value, argv = fp.parse(argv)
                    parsed_args[fp.spec.name] = value
                    break  # -> move on to the next arg

            else:
                raise ValueError(f"Unknown option: '{argv[0]}'")

        return parsed_args

    @classmethod
    def _read_args_from_file(cls, spec: config_spec.ConfigSpec, file_path: str) -> typing.Dict[str, typing.Any]:
        """Parses a JSON file into dictionary of configuration values.

        Args:
            spec (:class:`config_spec.ConfigSpec`): The spec that describes the configuration that needs to be parsed.
            file_path (str): The path of the JSON file to parse.

        Returns:
            dict: The parsed configuration.

        Raises:
            ValueError: If the ``file_path`` does not exist or refers to file of another format than JSON, if an unknown
                arg is encountered, or if parsing any arg fails for some reason.
        """

        # ensure that the config file exists
        if not os.path.isfile(file_path):
            raise ValueError(f"Config file not found: '{file_path}'")

        # read the json file
        try:
            with open(file_path, "r") as f:
                json_data = json.load(f)
        except json.decoder.JSONDecodeError:
            raise ValueError(f"The specified config file is not a valid JSON file: '{file_path}'")

        # ensure that the json file describes a dict of config values
        if not isinstance(json_data, dict):
            raise ValueError("The config file does not describe a dictionary of config values")

        # create parsers for all config values
        field_parsers = {p.spec.name: p for p in cls._create_parsers(spec)}

        # parse all args
        parsed_args = {}
        for config_name, config_value in json_data.items():  # -> iterate over all config values in the file

            # ensure that the encountered config exists
            if config_name not in field_parsers:
                raise ValueError(f"Unknown option: '{config_name}'")

            # parse the value
            parsed_args[config_name] = field_parsers[config_name].parse_json(config_value)

        return parsed_args

    def parse_args(self) -> typing.Any:
        """Parses the args of the current application based on the configuration class that was handed to the
        ``MagiqParser``, and returns an instance of this very class that has been populated accordingly.

        Returns:
            The parsed configuration or ``None``, if the help text has been requested.
        """

        # generate the config spec from the used configuration class
        spec = config_spec.ConfigSpec.create_from(self._spec)

        # check whether the help text should be printed instead of parsing args
        if "-h" in sys.argv[1:] or "--help" in sys.argv[1:]:

            self._print_help_text(spec)
            return None

        # check whether the args have to be parsed from the command line or read from a json file
        read_from_file = len(sys.argv) == 3 and sys.argv[1] == "--"
        if read_from_file:  # -> args have to be read from a json file

            parsed_args = self._read_args_from_file(spec, sys.argv[2])

        else:  # -> args have to be parsed from the command line

            parsed_args = self._read_args_from_command_line(
                    spec,
                    tuple(sys.argv[1:])  # -> we just remove the name of the application
            )

        # ensure that all required args have been provided
        for value_spec in spec:
            if value_spec.required and value_spec.name not in parsed_args:

                arg_name = (
                        value_spec.name
                        if read_from_file
                        else data_type_parser.DataTypeParser.translate_config_name(value_spec.name)
                )
                raise ValueError(f"Missing required arg {arg_name}")

        # create config object based on the parsed args
        config = self._spec()
        for config_name, config_value in parsed_args.items():
            setattr(config, config_name, config_value)

        return config
