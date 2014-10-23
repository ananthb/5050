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

from google.appengine.ext import ndb


class RandomURL(ndb.Model):

    """Stores the two URLs to forward to and number of redirects issued

    Fields:
      url1: Link to the first URL
      url2: Link to the second URL
      all_views: Total number of redirects issued
      views_for_1: Redirects for the first URL
      views_for_2: Redirects for the second URL

    """

    title = ndb.StringProperty(default="Unicorn Rainbows")
    url1 = ndb.StringProperty(required=True)
    url2 = ndb.StringProperty(required=True)
    all_views = ndb.IntegerProperty()
    views_for_one = ndb.IntegerProperty()
    views_for_two = ndb.IntegerProperty()
