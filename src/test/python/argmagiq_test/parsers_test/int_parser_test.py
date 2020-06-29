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


import unittest

import argmagiq.parsers.int_parser as int_parser
import argmagiq.value_spec as value_spec


__author__ = "Patrick Hohenecker"
__copyright__ = "Copyright (c) 2020, Patrick Hohenecker"
__license__ = "BSD-2-Clause"
__version__ = "0.1.0"
__date__ = "29 Jun 2020"
__maintainer__ = "Patrick Hohenecker"
__email__ = "patrick.hohenecker@gmx.at"
__status__ = "Development"


class IntParserTest(unittest.TestCase):

    #  TEST: _parse  ###################################################################################################

    def test_parse_raises_a_value_error_if_an_expected_value_is_missing(self):

        parser = int_parser.IntParser(value_spec.ValueSpec("some_config", "Just a test", int, True, None))
        argv = "--some-config",

        self.assertTrue(parser.fires(argv))
        with self.assertRaises(ValueError):
            parser._parse(argv)

    def test_parse_raises_a_value_error_if_an_illegal_value_is_provided(self):

        parser = int_parser.IntParser(value_spec.ValueSpec("some_config", "Just a test", int, True, None))
        argv = "--some-config", "not-a-number"

        self.assertTrue(parser.fires(argv))
        with self.assertRaises(ValueError):
            parser._parse(argv)

    def test_parse_extracts_legal_integer_args_as_expected(self):

        parser = int_parser.IntParser(value_spec.ValueSpec("some_config", "Just a test", int, True, None))

        value, argv = parser._parse(("--some-config", "666", "--another-config", "another value"))
        self.assertIsInstance(value, int)
        self.assertEqual((666, ("--another-config", "another value")), (value, argv))

        value, argv = parser._parse(("--some-config", "666"))
        self.assertIsInstance(value, int)
        self.assertEqual((666, tuple()), (value, argv))
