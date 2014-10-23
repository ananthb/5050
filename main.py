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

import webapp2
from handlers import IndexHandler, RedirectHandler, ViewsUpdateBot


app = webapp2.WSGIApplication(
    routes=[
        webapp2.Route(r'/', handler=IndexHandler),
        webapp2.Route(r'/<url_id:[a-zA-Z0-9]*>', handler=RedirectHandler),
        webapp2.Route(r'/update-views', handler=ViewsUpdateBot)
    ],
    debug=False,
)
