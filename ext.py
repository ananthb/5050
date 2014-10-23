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

import os
import random
import string

def debug():
    """Returns True if running locally, else False"""

    return os.getenv('SERVER_SOFTWARE').startswith('Dev')

def id_generator(
    size=5,
    chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):

    """Random string generator

    Accepts size and characters parameters. Returns a string of
    given size (defaults to 5) composed of random characters from
    the characters input. Characters defaults to lowercase and
    uppercase alphabets and digits.

    """

    return ''.join(random.choice(chars) for x in range(size))
