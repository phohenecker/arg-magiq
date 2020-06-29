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
import unittest

import argmagiq.parsers.data_type_parser as data_type_parser
import argmagiq.value_spec as value_spec


__author__ = "Patrick Hohenecker"
__copyright__ = "Copyright (c) 2020, Patrick Hohenecker"
__license__ = "BSD-2-Clause"
__version__ = "0.1.0"
__date__ = "29 Jun 2020"
__maintainer__ = "Patrick Hohenecker"
__email__ = "patrick.hohenecker@gmx.at"
__status__ = "Development"


class DataTypeParserTest(unittest.TestCase):

    #  TEST: fires  ####################################################################################################

    def test_fires_yields_the_expected_values(self):

        parser = _DummyParser(value_spec.ValueSpec("some_config", "Just a test", str, True, None))

        self.assertTrue(parser.fires(("--some-config",)))
        self.assertTrue(parser.fires(("--some-config", "value")))
        self.assertFalse(parser.fires(("--smth-else-first", "--some-config", "value")))
        self.assertFalse(parser.fires(("smth different entirely",)))

    #  TEST: parse  ####################################################################################################

    def test_parse_raises_a_value_error_if_the_parser_does_not_fire(self):

        parser = _DummyParser(value_spec.ValueSpec("some_config", "Just a test", str, True, None))

        with self.assertRaises(ValueError):
            parser.parse(("--smth-else-first", "--some-config", "value"))
        with self.assertRaises(ValueError):
            parser.parse(("smth different entirely",))

    #  TEST: parse_json  ###############################################################################################

    def test_parse_json_raises_a_type_error_if_the_provided_value_does_not_comply_with_the_spec(self):

        parser = _DummyParser(value_spec.ValueSpec("some_config", "Just a test", str, True, None))

        with self.assertRaises(TypeError):
            parser.parse_json(123)

    def test_parse_json_returns_the_provided_value_if_its_of_the_correct_type(self):

        parser = _DummyParser(value_spec.ValueSpec("some_config", "Just a test", str, True, None))

        self.assertEqual("works", parser.parse_json("works"))


class _DummyParser(data_type_parser.DataTypeParser):

    def _parse(self, argv: typing.Tuple[str, ...]) -> typing.Tuple[typing.Any, typing.Tuple[str, ...]]:

        return "nothing", argv
