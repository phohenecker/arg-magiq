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


import sys
import unittest
import unittest.mock as mock

import argmagiq.config_spec as config_spec
import argmagiq.magiq_parser as magiq_parser
import argmagiq.value_spec as value_spec


__author__ = "Patrick Hohenecker"
__copyright__ = "Copyright (c) 2020, Patrick Hohenecker"
__license__ = "BSD-2-Clause"
__version__ = "0.1.0"
__date__ = "29 Jun 2020"
__maintainer__ = "Patrick Hohenecker"
__email__ = "patrick.hohenecker@gmx.at"
__status__ = "Development"


class MagiqParserTest(unittest.TestCase):

    def setUp(self):

        self.spec = config_spec.ConfigSpec()
        self.spec.add_value(value_spec.ValueSpec("conf_1", "No description available.", bool, False, False))
        self.spec.add_value(value_spec.ValueSpec("conf_2", "No description available.", int, True, None))

        self.parser = magiq_parser.MagiqParser(_TestConfig, "name", "description")

    #  TEST: _read_args_from_command_line  #############################################################################

    def test_read_args_from_command_line_parses_args_correctly(self):

        parsed_args = magiq_parser.MagiqParser._read_args_from_command_line(
                self.spec,
                ("--conf-1", "--conf-2", "666")
        )
        self.assertEqual(
                {"conf_1": True, "conf_2": 666},
                parsed_args
        )

    def test_read_args_from_command_line_raises_a_value_error_if_an_unknown_arg_is_encountered(self):

        with self.assertRaises(ValueError):
            magiq_parser.MagiqParser._read_args_from_command_line(
                    self.spec,
                    ("--conf-1", "--this-one-does-not-exist", "--conf-2", "666")
            )

    #  TEST: _read_args_from_file  #####################################################################################

    def test_read_args_from_file_parses_args_correctly(self):

        parsed_args = magiq_parser.MagiqParser._read_args_from_file(
                self.spec,
                "src/test/resources/valid_test_config.json"
        )
        self.assertEqual(
                {"conf_1": True, "conf_2": 666},
                parsed_args
        )

    def test_read_args_from_file_raises_a_value_error_if_an_unknown_arg_is_encountered(self):

        with self.assertRaises(ValueError):
            magiq_parser.MagiqParser._read_args_from_file(
                    self.spec,
                    "src/test/resources/invalid_test_config.json"
            )

    def test_read_args_from_file_raises_a_value_error_if_the_config_file_does_not_exist(self):

        with self.assertRaises(ValueError):
            magiq_parser.MagiqParser._read_args_from_file(self.spec, "/does/not/exist.json")

    #  TEST: parse_args  ###############################################################################################

    def test_parse_args_invokes_the_right_method_for_parsing_args(self):

        parsed_args = {"conf_1": True, "conf_2": 666}

        with mock.patch.object(
                magiq_parser.MagiqParser,
                "_read_args_from_command_line",
                return_value=parsed_args
        ) as mock_method:

            sys.argv = ["app", "--conf-1", "--conf-2", "666"]
            self.parser.parse_args()

        mock_method.assert_called_once_with(self.spec, ("--conf-1", "--conf-2", "666"))

        with mock.patch.object(
                magiq_parser.MagiqParser,
                "_read_args_from_file",
                return_value=parsed_args
        ) as mock_method:

            sys.argv = ["app", "--", "/src/main/resources/valid_test_config.json"]
            self.parser.parse_args()

        mock_method.assert_called_once_with(self.spec, "/src/main/resources/valid_test_config.json")


class _TestConfig(object):

    DEFAULT_CONF_1 = False

    def __init__(self):

        self._conf_1 = self.DEFAULT_CONF_1
        self._conf_2 = None

    @property
    def conf_1(self) -> bool:
        return self._conf_1

    @conf_1.setter
    def conf_1(self, conf_1: bool) -> None:
        self._conf_1 = conf_1

    @property
    def conf_2(self) -> int:
        return self._conf_2

    @conf_2.setter
    def conf_2(self, conf_2: int) -> None:
        self._conf_2 = conf_2
