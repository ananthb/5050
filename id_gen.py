#!/usr/bin/env python
#
# Copyright (C) 2013 Ananth Bhaskararaman
# This file is part of 5050.
#
# 5050 URL roulette is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# 5050 is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with 5050.  If not, see <http://www.gnu.org/licenses/>.
#

import random
import string

ALL_THE_LETTERS = string.ascii_letters + string.digits


def generate(size=5, chars=ALL_THE_LETTERS):

    """Random string generator

    Accepts size and characters parameters. Returns a string of
    given size (defaults to 5) composed of random characters from
    the characters input. Characters default to lowercase and
    uppercase alphabets, and digits.

    """

    return ''.join(random.choice(chars) for x in range(size))
