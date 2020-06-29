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

import argmagiq


__author__ = "Patrick Hohenecker"
__copyright__ = "Copyright (c) 2020, Patrick Hohenecker"
__license__ = "BSD-2-Clause"
__version__ = "0.1.0"
__date__ = "29 Jun 2020"
__maintainer__ = "Patrick Hohenecker"
__email__ = "patrick.hohenecker@gmx.at"
__status__ = "Development"


class InitTest(unittest.TestCase):

    #  TEST: extract_config  ###########################################################################################

    def test_extract_config_raises_a_type_error_if_none_is_provided(self):

        with self.assertRaises(TypeError):
            argmagiq.extract_config(None)

    def test_extract_config_extracts_the_expected_values(self):

        class _Config(object):

            DEFAULT_CONF_1 = 123

            def __init__(self):
                self._conf_1 = self.DEFAULT_CONF_1
                self._conf_2 = None
                self._conf_3 = None

            @property
            def conf_1(self) -> int:
                return self._conf_1

            @conf_1.setter
            def conf_1(self, conf_1: int) -> None:
                self._conf_1 = conf_1

            @property
            def conf_2(self) -> str:
                return self._conf_2

            @conf_2.setter
            def conf_2(self, conf_2: str) -> None:
                self._conf_2 = conf_2

            @argmagiq.optional
            @property
            def conf_3(self) -> typing.Optional[str]:
                return self._conf_3

            @conf_3.setter
            def conf_3(self, conf_3: str) -> None:
                self._conf_3 = conf_3

        conf = _Config()
        conf.conf_2 = "abc"

        self.assertEqual(
                {"conf_1": 123, "conf_2": "abc", "conf_3": None},
                argmagiq.extract_config(conf)
        )
