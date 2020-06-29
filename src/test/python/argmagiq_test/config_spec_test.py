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
import typing

import argmagiq
import argmagiq.config_spec as config_spec
import argmagiq.value_spec as value_spec


__author__ = "Patrick Hohenecker"
__copyright__ = "Copyright (c) 2020, Patrick Hohenecker"
__license__ = "BSD-2-Clause"
__version__ = "0.1.0"
__date__ = "29 Jun 2020"
__maintainer__ = "Patrick Hohenecker"
__email__ = "patrick.hohenecker@gmx.at"
__status__ = "Development"


class ConfigSpecTest(unittest.TestCase):

    #  TEST: add_value  ################################################################################################

    def test_add_value_raises_a_type_error_if_args_of_an_illegal_type_are_provided(self):

        spec = config_spec.ConfigSpec()

        with self.assertRaises(TypeError):
            spec.add_value(None)
        with self.assertRaises(TypeError):
            spec.add_value("value")

    def test_add_value_stores_value_specs_as_expected(self):

        spec = config_spec.ConfigSpec()
        value_1 = value_spec.ValueSpec("val-1", "val-1", str, False, None)
        value_2 = value_spec.ValueSpec("val-2", "val-2", str, False, None)

        self.assertEqual(0, len(spec))

        spec.add_value(value_1)
        self.assertEqual(1, len(spec))
        self.assertEqual({value_1}, set(spec))

        spec.add_value(value_2)
        self.assertEqual(2, len(spec))
        self.assertEqual({value_1, value_2}, set(spec))

    #  TEST: create_from  ##############################################################################################

    def test_create_from_all_supported_data_types_correctly(self):

        class _Config(object):

            DEFAULT_BOOL = True

            def __init__(self):
                self._bool = self.DEFAULT_BOOL
                self._float = None
                self._int = None
                self._str = None

            @property
            def bool(self) -> bool:
                return self._bool

            @bool.setter
            def bool(self, x: bool) -> None:
                self._bool = x

            @property
            def float(self) -> float:
                return self._float

            @float.setter
            def float(self, x: float) -> None:
                self._float = x

            @property
            def int(self) -> int:
                return self._int

            @int.setter
            def int(self, x: int) -> None:
                self._int = x

            @property
            def str(self) -> str:
                return self._str

            @str.setter
            def str(self, x: str) -> None:
                self._str = x

        spec = config_spec.ConfigSpec.create_from(_Config)
        self.assertEqual(4, len(spec))
        self.assertEqual(
                value_spec.ValueSpec("bool", "No description available.", bool, False, True),
                spec.get_value_by_name("bool")
        )
        self.assertEqual(
                value_spec.ValueSpec("float", "No description available.", float, True, None),
                spec.get_value_by_name("float")
        )
        self.assertEqual(
                value_spec.ValueSpec("int", "No description available.", int, True, None),
                spec.get_value_by_name("int")
        )
        self.assertEqual(
                value_spec.ValueSpec("str", "No description available.", str, True, None),
                spec.get_value_by_name("str")
        )

    def test_create_from_the_generic_optional_alias_correctly(self):

        class _Config(object):

            DEFAULT_CONF_WITH_DEFAULT_VALUE = 123

            def __init__(self):
                self._value = None

            @property
            def value(self) -> typing.Optional[int]:
                return self._value

            @value.setter
            def value(self, value: int) -> None:
                self._value = value

        spec = config_spec.ConfigSpec.create_from(_Config)
        self.assertEqual(1, len(spec))
        self.assertEqual(
                value_spec.ValueSpec("value", "No description available.", int, True, None),
                spec.get_value_by_name("value")
        )

    def test_create_from_raises_a_value_error_if_an_unsupported_generic_alias_is_encountered(self):

        class _Config(object):

            def __init__(self):
                self._value = None

            @property
            def value(self) -> typing.Union[int, str]:
                return self._value

            @value.setter
            def value(self, value: typing.Union[int, str]) -> None:
                self._value = value

        with self.assertRaises(ValueError):
            config_spec.ConfigSpec.create_from(_Config)

    def test_create_from_determines_correctly_whether_a_config_is_required_or_optional(self):

        class _Config(object):

            DEFAULT_CONF_WITH_DEFAULT_VALUE = 123

            def __init__(self):
                self._conf_with_default_value = self.DEFAULT_CONF_WITH_DEFAULT_VALUE
                self._conf_without_default_value = None
                self._optional_conf_without_default_value = None

            @property
            def conf_with_default_value(self) -> int:
                return self._conf_with_default_value

            @conf_with_default_value.setter
            def conf_with_default_value(self, conf_with_default_value: int) -> None:
                self._conf_with_default_value = conf_with_default_value

            @property
            def conf_without_default_value(self) -> str:
                return self._conf_without_default_value

            @conf_without_default_value.setter
            def conf_without_default_value(self, conf_without_default_value: str) -> None:
                self._conf_without_default_value = conf_without_default_value

            @argmagiq.optional
            @property
            def optional_conf_without_default_value(self) -> typing.Optional[float]:
                return self._optional_conf_without_default_value

            @optional_conf_without_default_value.setter
            def optional_conf_without_default_value(self, optional_conf_without_default_value: float) -> None:
                self._optional_conf_without_default_value = optional_conf_without_default_value

        spec = config_spec.ConfigSpec.create_from(_Config)
        self.assertEqual(3, len(spec))
        self.assertFalse(spec.get_value_by_name("conf_with_default_value").required)
        self.assertTrue(spec.get_value_by_name("conf_without_default_value").required)
        self.assertFalse(spec.get_value_by_name("optional_conf_without_default_value").required)

    def test_create_extracts_descriptions_correctly(self):

        class _Config(object):

            def __init__(self):
                self._conf_without_description = None
                self._conf_with_description_1 = None
                self._conf_with_description_2 = None

            @property
            def conf_without_description(self) -> int:
                return self._conf_without_description

            @conf_without_description.setter
            def conf_without_description(self, conf_without_description: int) -> None:
                self._conf_without_description = conf_without_description

            @property
            def conf_with_description_1(self) -> int:
                """This is description 1."""
                return self._conf_with_description_1

            @conf_with_description_1.setter
            def conf_with_description_1(self, conf_with_description_1: int) -> None:
                self._conf_with_description_1 = conf_with_description_1

            @property
            def conf_with_description_2(self) -> int:
                """int: This is description 2, which includes the type at the beginning."""
                return self._conf_with_description_2

            @conf_with_description_2.setter
            def conf_with_description_2(self, conf_with_description_2: int) -> None:
                self._conf_with_description_2 = conf_with_description_2

        spec = config_spec.ConfigSpec.create_from(_Config)
        self.assertEqual(3, len(spec))
        self.assertEqual(
                "No description available.",
                spec.get_value_by_name("conf_without_description").description
        )
        self.assertEqual(
                "This is description 1.",
                spec.get_value_by_name("conf_with_description_1").description
        )
        self.assertEqual(
                "This is description 2, which includes the type at the beginning.",
                spec.get_value_by_name("conf_with_description_2").description
        )

    def test_create_from_extracts_default_values_correctly(self):

        class _Config(object):

            DEFAULT_CONF_WITH_DEFAULT_VALUE = 123

            def __init__(self):
                self._conf_with_default_value = self.DEFAULT_CONF_WITH_DEFAULT_VALUE
                self._conf_without_default_value = None

            @property
            def conf_with_default_value(self) -> int:
                return self._conf_with_default_value

            @conf_with_default_value.setter
            def conf_with_default_value(self, conf_with_default_value: int) -> None:
                self._conf_with_default_value = conf_with_default_value

            @property
            def conf_without_default_value(self) -> str:
                return self._conf_without_default_value

            @conf_without_default_value.setter
            def conf_without_default_value(self, conf_without_default_value: str) -> None:
                self._conf_without_default_value = conf_without_default_value

        spec = config_spec.ConfigSpec.create_from(_Config)
        self.assertEqual(2, len(spec))
        self.assertEqual(123, spec.get_value_by_name("conf_with_default_value").default_value)
        self.assertIsNone(spec.get_value_by_name("conf_without_default_value").default_value)

    #  TEST: get_value_by_name  ########################################################################################

    def test_get_value_by_name_retrieves_existing_config_values_as_expected(self):

        spec = config_spec.ConfigSpec()
        value = value_spec.ValueSpec("val", "val", str, False, None)
        spec.add_value(value)

        self.assertIs(value, spec.get_value_by_name("val"))

    def test_get_value_by_name_retrieves_none_for_non_existing_values(self):

        spec = config_spec.ConfigSpec()
        self.assertIsNone(spec.get_value_by_name("val"))
