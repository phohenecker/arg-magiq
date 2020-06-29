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


"""This is an example that illustrates the basic usage of ``argmagiq``.

To try this code, run the following commands in your terminal:

.. code-block:: bash

   $ python3 sum.py --x 100 --y 50 --weight-y 4 --label value
   value = 2 * (100.0 + 4.0 * 50.0) = 600.0

.. code-block:: bash

   $ python3 sum.py -- sum-config.json
   value = 2 * (100.0 + 4.0 * 50.0) = 600.0

"""


import typing

import argmagiq


__author__ = "Patrick Hohenecker"
__copyright__ = "Copyright (c) 2020, Patrick Hohenecker"
__license__ = "BSD-2-Clause"
__version__ = "0.1.0"
__date__ = "29 Jun 2020"
__maintainer__ = "Patrick Hohenecker"
__email__ = "patrick.hohenecker@gmx.at"
__status__ = "Development"


# ==================================================================================================================== #
#  CONFIG CLASS                                                                                                        #
# ==================================================================================================================== #


class Config(object):

    DEFAULT_DOUBLE = False  # -> makes --double optional with default value False
    DEFAULT_WEIGHT_X = 1.0  # -> makes --weight-x optional with default value 1.0
    DEFAULT_WEIGHT_Y = 1.0  # -> makes --weight-y optional with default value 1.0

    #  CONSTRUCTOR  ####################################################################################################

    def __init__(self):

        self._double = self.DEFAULT_DOUBLE
        self._label = None
        self._weight_x = self.DEFAULT_WEIGHT_X
        self._weight_y = self.DEFAULT_WEIGHT_Y
        self._x = None
        self._y = None

    #  PROPERTIES  #####################################################################################################

    @property  # -> defines arg --double (together with the according setter)
    def double(self) -> bool:  # -> specifies bool as the type of arg --double
        """bool: Specifies that the sum should be doubled."""
        return self._double

    @double.setter
    def double(self, double: bool) -> None:
        self._double = bool(double)

    @argmagiq.optional  # -> makes arg --label optional, even though it does NOT have a default value
    @property  # -> defines arg --label (together with the according setter)
    def label(self) -> typing.Optional[str]:  # -> specifies str as the type of arg --label
        """str: A label to print with the formula."""
        return self._label

    @label.setter
    def label(self, label: typing.Optional[str]) -> None:
        self._label = label

    @property  # -> defines arg --weight-x (together with the according setter)
    def weight_x(self) -> float:  # -> specifies float as the type of arg --weight-x
        """float: A multiplier for x."""
        return self._weight_x

    @weight_x.setter
    def weight_x(self, weight_x: float) -> None:
        self._weight_x = weight_x

    @property  # -> defines arg --weight-y (together with the according setter)
    def weight_y(self) -> float:  # -> specifies float as the type of arg --weight-y
        """float: A multiplier for y."""
        return self._weight_y

    @weight_y.setter
    def weight_y(self, weight_y: float) -> None:
        self._weight_y = weight_y

    @property  # -> defines arg --x (together with the according setter)
    def x(self) -> float:  # -> specifies float as the type of arg --x
        """float: The first number to add."""
        return self._x

    @x.setter
    def x(self, x: float) -> None:
        self._x = x

    @property  # -> defines arg --y (together with the according setter)
    def y(self) -> float:  # -> specifies float as the type of arg --y
        """float: The second number to add."""
        return self._y

    @y.setter
    def y(self, y: float) -> None:
        self._y = y


# ==================================================================================================================== #
#  MAIN                                                                                                                #
# ==================================================================================================================== #


def main(args: typing.Optional[Config]):

    if args is None:  # -> help text was printed
        return

    result = 0

    if args.label:
        print(f"{args.label} = ", end="")

    if args.double:
        print("2 * (", end="")

    if args.weight_x == 1:
        result += args.x
    else:
        result += args.x * args.weight_x
        print(f"{args.weight_x} * ", end="")

    print(f"{args.x} + ", end="")

    if args.weight_y == 1:
        result += args.y
    else:
        result += args.y * args.weight_y
        print(f"{args.weight_y} * ", end="")

    if args.double:
        print(f"{args.y}) = {2 * result}")
    else:
        print(f"{args.y} = {result}")


if __name__ == "__main__":

    try:

        main(
                argmagiq.parse_args(
                        Config,
                        "sum",
                        "This application sums to numbers, x and y."
                )
        )

    except ValueError as e:

        print(e)
