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

from __future__ import division

import os
import logging
import traceback
import random
import json
import re

import webapp2
import jinja2
from google.appengine.api import taskqueue

import ext
from models import RandomURL


class BaseHandler(webapp2.RequestHandler):

    """Extends webapp2.RequestHandler to provide useful methods

    Request handlers inherit from this handler. Contains methods
    for rendering jinja2 templates and handling exceptions raised by
    other request handlers.

    """


    @webapp2.cached_property
    def jinja_env(self):
        return jinja2.Environment(
            loader = jinja2.FileSystemLoader(
                os.path.dirname(__file__)
                ),
                trim_blocks=True
            )

    def render(self, template_name, values={}):
        """Renders the template with the values dict"""

        if ext.debug():
            values.update(host='http://' + os.environ['HTTP_HOST'])
        else:
            values.update(host='http://5050.me')

        template = self.jinja_env.get_template(template_name)
        self.response.out.write(template.render(values))

    def handle_exception(self, exception, debug):
        """Handles exceptions raised by the methods of request handlers.

        The method logs the exception and sets the appropriate
        HTTP status code. If debug is True, the stack trace for
        the exception is sent as the response. Otherwise a generic
        error page is sent.

        """

        logging.exception(exception)

        if isinstance(exception, webapp2.HTTPException):
            self.response.set_status(exception.code)
        else:
            self.response.set_status(500)

        if debug:
            values = {
                'title': 'Error',
                'traceback': traceback.format_exc().splitlines()
                }
        else:
            values = {
                'title': 'Oompa Loompa Error',
                'error': True
                }
        self.render('template.html', values)

class IndexHandler(BaseHandler):

    """Displays form for accepting links.

    If the id parameter is present, a summary page with number
    of visits and other statistics is shown.

    """


    def get(self):
        values = {
            'title': 'Fifty Fifty Link Roulette',
            }

        url_id = self.request.get('id')
        if url_id:
            url = RandomURL.get_by_id(url_id)
            if not url:
                self.abort(404)

            url_views = {
                'url1': url.url1,
                'for_one': url.views_for_one,
                'url2': url.url2,
                'for_two': url.views_for_two
            }

            if url.all_views:
                r1 = int(url.views_for_one / url.all_views * 100)
                r2 = 100 - r1
                ratio = '{}% : {}%'.format(r1, r2)
            else:
                ratio = None

            values.update(
                url_title=url.title,
                all_views=url.all_views,
                url_id=url_id,
                views=url_views,
                ratio=ratio,
                )
        self.render('template.html', values)

    def post(self):
        title = self.request.get('title')
        url1 = self.request.get('url1')
        url2 = self.request.get('url2')

        if not (url1 or url2):
            self.abort(400)

        p = re.compile(r'^https?://')
        if not p.search(url1):
            url1 = 'http://' + url1
        if not p.search(url2):
            url2 = 'http://' + url2

        url = 'Some random url'
        while url:
            rand_id = ext.id_generator()
            url = RandomURL.get_by_id(rand_id)

        new_urls = RandomURL(id=rand_id, url1=url1, url2=url2)
        if title:
            new_urls.title = title
        new_urls.put()
        self.redirect('/?id={}'.format(rand_id))

class RedirectHandler(BaseHandler):

    """Redirects the client to one of two links

    The entity with the key matching the given id is
    retreived from the databse. A random choice is made and a
    redirect is issued. The view stats are sent to a taskqueue
    for processing.

    """

    def get(self, url_id):
        if len(url_id) != 5:
            self.abort(404)

        urls = RandomURL.get_by_id(url_id)
        if not urls:
            self.abort(404)

        if random.random() < 0.5:
            payload = {'id': url_id,
                       'index': 1}
            self.redirect(str(urls.url1))
        else:
            payload = {'id': url_id,
                       'index': 2}
            self.redirect(str(urls.url2))
        taskqueue.add(
                payload = json.dumps(payload),
                queue_name='views',
                method='PULL'
                )

class ViewsUpdateBot(BaseHandler):

    """Task queue worker to update the views"""

    def get(self):
        q = taskqueue.Queue('views')
        tasks = q.lease_tasks(360, 100)
        if not tasks:
            logging.info('No views to update')
            return

        stats = {}
        for task in tasks:
            payload = json.loads(task.payload)
            url_id = payload['id']
            if not stats.has_key(url_id):
                stats.update({url_id: {'one': 0, 'two': 0}})
            if payload['index'] == 1:
                stats[payload['id']]['one'] += 1
            elif payload['index'] == 2:
                stats[payload['id']]['two'] += 1

        for u_id in stats.iterkeys():
            url = RandomURL.get_by_id(u_id)
            url.views_for_one = stats[u_id]['one']
            url.views_for_two = stats[u_id]['two']
            url.all_views = stats[u_id]['one'] + stats[u_id]['two']
            url.put()
        q.delete_tasks(tasks)
