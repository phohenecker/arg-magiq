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


"""A Python library for parsing command-line args automagically."""


import inspect
import typing

from argmagiq.decorators import *
from argmagiq.magiq_parser import MagiqParser
from argmagiq.parsers.data_type_parser import DataTypeParser


__author__ = "Patrick Hohenecker"
__copyright__ = "Copyright (c) 2020, Patrick Hohenecker"
__license__ = "BSD-2-Clause"
__version__ = "0.1.0"
__date__ = "29 Jun 2020"
__maintainer__ = "Patrick Hohenecker"
__email__ = "patrick.hohenecker@gmx.at"
__status__ = "Development"


DEFAULT_PREFIX = "DEFAULT_"
"""str: A prefix that identifies class variables as default values."""

TEXT_WIDTH = 80
"""int: The maximum text width used for printing the help text."""


def extract_config(conf: typing.Any) -> typing.Dict[str, typing.Any]:
    """Creates a ``dict`` that summarizes the values stored in a configuration object.

    As usual, this function considers all public mutable properties.

    Args:
        conf: The object that contains the configuration to extract.

    Returns:
        dict: Maps the names of the considered members to their according values.
    """

    if conf is None:
        raise TypeError("<conf> must not be None!")

    str_conf = {}  # -> used to store the extracted configuration

    # find all public mutable properties -> these are considered as config values
    for name, field in inspect.getmembers(type(conf), lambda f: isinstance(f, property)):

        # only consider public properties that have an according setter method
        if not name.startswith("_") and field.fset is not None:
            str_conf[name] = getattr(conf, name)

    return str_conf


def parse_args(
        conf_class: type,
        app_name: str = None,
        app_description: str = None
):
    """Parses the args of the current application based on the provided configuration class, and returns an instance of
    the same that is populated accordingly.

    Args:
        conf_class (type): The configuration class that specifies the command line args to parse.
        app_name (str): The name of the application that is printed in the synopsis.
        app_description (str): The description of the application that is printed in the synopsis.

    Returns:
        The parsed configuration as an object of type ``conf_class``.
    """
    return MagiqParser(
            conf_class,
            app_name=app_name,
            app_description=app_description
    ).parse_args()
